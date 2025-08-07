import base64
import csv
import json

from Crypto.Cipher import AES

from piicrypto.helpers.logger_helper import setup_logger
from piicrypto.helpers.utils import (
    find_best_match,
    generate_metadata,
    generate_nonce,
    skip_id_column,
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
    aliases_file: str = None,
    create_metadata: bool = False,
    skip_fields: str = None,
):
    """
    Encrypt specified fields in a CSV file using AES encryption.
    """
    logger.info(f"Starting Encryption process for {input_file} to {output_file}")
    key_manager = KeyManager(mode, key_provider_config)
    version, keys = key_manager.load_latest_keys()
    logger.info(
        f"Loaded keys for mode: {mode}, for version: {version} from {key_provider_config}"
    )
    fields_to_skip = skip_fields.split(",") if skip_fields else []
    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ["row_iv"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        encrypted_fields = set()
        for row_num, row in enumerate(reader):
            nonce = generate_nonce()
            for field in reader.fieldnames:
                if not row[field] or skip_id_column(row_num, row[field], field):
                    logger.info(f"Skipping field: {field} in row {row_num}")
                    continue
                field_alias = (
                    find_best_match(field, aliases_file) if aliases_file else field
                )
                if field_alias in fields_to_skip:
                    logger.info(f"Skipping field: {field_alias} in row {row_num}")
                    continue
                if field_alias in keys:
                    row[field] = f"{version}:" + encrypt_data(
                        keys[field_alias], row[field], nonce
                    )
                    encrypted_fields.add(field)
                    logger.info(f"Encrypted field: {field_alias} in row {row_num}")
            row["row_iv"] = base64.b64encode(nonce).decode()
            writer.writerow(row)
    if create_metadata:
        metadata = generate_metadata(
            keys_version=version,
            out_file=output_file,
            mode=mode,
            operation="encrypt",
            operation_fields=encrypted_fields,
        )
        with open(f"{output_file}.metadata.json", "w") as meta_file:
            json.dump(metadata, meta_file, indent=4)
        logger.info(f"Metadata saved to {output_file}.metadata.json")
    logger.info(f"CSV file encrypted successfully at {output_file}.")
