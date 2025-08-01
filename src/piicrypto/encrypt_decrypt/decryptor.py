import base64
import csv

from Crypto.Cipher import AES

from piicrypto.helpers.logger_helper import setup_logger
from piicrypto.helpers.utils import find_best_match
from piicrypto.key_provider.base_key_provider import BaseKeyProvider

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
    key_provider: BaseKeyProvider,
    aliases_file: str = None,
):
    """
    Decrypt specified fields in a CSV file using AES decryption.
    """
    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            for field in fieldnames:
                if field == "row_iv" or not row[field] or ":" not in row[field]:
                    continue
                field_alias = (
                    find_best_match(field, aliases_file) if aliases_file else field
                )
                version, encrypted_data = row[field].split(":")
                keys = key_provider.get_keys_by_version(version)
                if not keys:
                    raise ValueError(f"No keys found for version {version}")
                if field_alias in keys:
                    try:
                        row[field] = decrypt_data(
                            keys[field_alias], encrypted_data, nonce=row["row_iv"]
                        )
                    except Exception as e:
                        logger.info(f"Error decrypting field '{field}': {e}")
                        row[field] = f"{row[field]} Decryption Error"
            writer.writerow(row)
