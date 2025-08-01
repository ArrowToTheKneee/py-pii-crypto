import base64
import csv

from Crypto.Cipher import AES

from piicrypto.helpers.utils import find_best_match, generate_nonce, skip_id_column
from piicrypto.key_provider.key_manager import load_latest_keys


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
    input_file: str, output_file: str, keys_file: str, aliases_file: str = None
):
    """
    Encrypt specified fields in a CSV file using AES encryption.
    """
    version, keys = load_latest_keys(keys_file)
    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ["row_iv"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row_num, row in enumerate(reader):
            nonce = generate_nonce()
            for field in reader.fieldnames:
                if not row[field] or skip_id_column(row_num, row[field], field):
                    continue
                field_alias = (
                    find_best_match(field, aliases_file) if aliases_file else field
                )
                if field_alias in keys:
                    row[field] = f"{version}:" + encrypt_data(
                        keys[field_alias], row[field], nonce
                    )
            row["row_iv"] = base64.b64encode(nonce).decode()
            writer.writerow(row)
