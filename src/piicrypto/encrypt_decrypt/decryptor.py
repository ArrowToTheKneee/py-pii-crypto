import base64
import csv
import json

from Crypto.Cipher import AES

from piicrypto.helpers.logger_helper import setup_logger
from piicrypto.helpers.utils import find_best_match, generate_metadata
from piicrypto.key_provider.key_manager import KeyManager

logger = setup_logger(name=__name__)


def decrypt_data(key: str, data: str, nonce: str) -> str:
    """
    Decrypt data using AES decryption for the specified field.
    """
    key = base64.b64decode(key.encode())
    data = base64.b64decode(data.encode())
    nonce = base64.b64decode(nonce.encode())
    tag = data[:16]
    ciphertext = data[16:]

    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)

    return decrypted_data.decode()


def decrypt_csv_file(
    input_file: str,
    output_file: str,
    mode: str,
    key_provider_config: str,
    create_metadata: bool = False,
):
    """
    Decrypt specified fields in a CSV file using AES decryption.
    """
    logger.info(f"Starting decryption process for {input_file} to {output_file}")
    key_manager = KeyManager(mode, key_provider_config)
    fields_to_alias = key_manager.field_to_alias
    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        decrypted_fields = set()
        for row in reader:
            for field in fieldnames:
                if field == "row_iv" or not row[field] or ":" not in row[field]:
                    logger.info(f"Skipping field: {field} in row {row}")
                    continue
                field_alias = (
                    find_best_match(field, fields_to_alias)
                    if fields_to_alias
                    else field
                )
                version, encrypted_data = row[field].split(":")
                keys = key_manager.get_keys_by_version(version)
                if not keys:
                    logger.error(f"No keys found for version {version}")
                    raise ValueError(f"No keys found for version {version}")
                if field_alias in keys:
                    try:
                        row[field] = decrypt_data(
                            keys[field_alias], encrypted_data, nonce=row["row_iv"]
                        )
                        decrypted_fields.add(field)
                        logger.info(f"Decrypted field: {field_alias} in row {row}")
                    except Exception as e:
                        logger.error(f"Error decrypting field '{field}': {e}")
                        row[field] = f"{row[field]} Decryption Error"
            writer.writerow(row)
    if create_metadata:
        metadata = generate_metadata(
            out_file=output_file,
            mode=mode,
            operation="decrypt",
            operation_fields=decrypted_fields,
        )
        with open(f"{output_file}.metadata.json", "w") as meta_file:
            json.dump(metadata, meta_file, indent=4)
        logger.info(f"Metadata saved to {output_file}.metadata.json")
    logger.info(f"CSV file decrypted successfully at {output_file}.")
