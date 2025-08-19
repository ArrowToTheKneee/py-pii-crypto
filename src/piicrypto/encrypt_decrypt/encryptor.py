import base64
import csv
import json

from Crypto.Cipher import AES

from piicrypto.helpers.create_dynamic_model import create_dynamic_model
from piicrypto.helpers.logger_helper import setup_logger
from piicrypto.helpers.utils import (
    find_best_match,
    generate_metadata,
    generate_nonce,
    skip_id_column,
    validate_row,
)
from piicrypto.key_provider.key_manager import KeyManager

logger = setup_logger(name=__name__)


def encrypt_data(key: str, data: str, nonce: bytes) -> str:
    """
    Encrypt data using AES encryption for the specified field.
    """
    key = base64.b64decode(key.encode())
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(data.encode())
    combined = base64.b64encode(tag + ciphertext).decode()
    return combined


def encrypt_csv_file(
    input_file: str,
    output_file: str,
    mode: str,
    key_provider_config: str,
    create_metadata: bool = False,
    validate_json: str = None,
):
    """
    Encrypt specified fields in a CSV file using AES encryption.
    """
    logger.info(f"Starting Encryption process for {input_file} to {output_file}")
    key_manager = KeyManager(mode, key_provider_config)
    keys = key_manager.load_keys()
    logger.info(f"Loaded keys for mode: {mode}, from {key_provider_config}")
    fields_to_encrypt = key_manager.fields_to_encrypt
    fields_to_alias = key_manager.field_to_alias
    validation_model = None
    if validate_json:
        validation_model = create_dynamic_model(validate_json)
        logger.info(f"Validation model created from {validate_json}")
    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ["row_iv"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        encrypted_fields = set()
        for row_num, row in enumerate(reader):
            if validation_model:
                logger.info(f"Validating row {row_num}")
                if not validate_row(row, validation_model):
                    logger.warning(f"Skipping row {row_num} due to validation errors")
                    continue
                logger.info(f"Row {row_num} validated successfully")
            logger.info(f"Processing row {row_num}")
            nonce = generate_nonce()
            for field in reader.fieldnames:
                if not row[field] or skip_id_column(row_num, row[field], field):
                    logger.info(f"Skipping field: {field} in row {row_num}")
                    continue
                field_alias = (
                    find_best_match(field, fields_to_alias)
                    if fields_to_alias
                    else field
                )
                if field_alias not in fields_to_encrypt:
                    logger.info(f"Skipping field: {field_alias} in row {row_num}")
                    continue
                if field_alias in keys:
                    version, key_material = keys[field_alias]
                    row[field] = f"{version}:" + encrypt_data(
                        key_material, row[field], nonce
                    )
                    encrypted_fields.add(field)
                    logger.info(f"Encrypted field: {field} in row {row_num}")
            row["row_iv"] = base64.b64encode(nonce).decode()
            logger.info(f"Processing completed for row {row_num}, writing to output")
            writer.writerow(row)
    if create_metadata:
        metadata = generate_metadata(
            out_file=output_file,
            mode=mode,
            operation="encrypt",
            operation_fields=encrypted_fields,
        )
        with open(f"{output_file}.metadata.json", "w") as meta_file:
            json.dump(metadata, meta_file, indent=4)
        logger.info(f"Metadata saved to {output_file}.metadata.json")
    logger.info(f"CSV file encrypted successfully at {output_file}.")
