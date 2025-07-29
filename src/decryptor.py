import base64
import csv

import typer
from Crypto.Cipher import AES

from key_manager import load_keys


def decrypt_data(key: str, data: str) -> str:
    """
    Decrypt data using AES decryption for the specified field.
    """
    key = base64.b64decode(key.encode())
    data = base64.b64decode(data.encode())
    nonce = data[:12]
    tag = data[12:28]
    ciphertext = data[28:]

    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)

    return decrypted_data.decode()


def decrypt_csv_file(input_file: str, output_file: str, keys_file: str):
    """
    Decrypt specified fields in a CSV file using AES decryption.
    """
    version, keys = load_keys(keys_file)
    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            for field in fieldnames:
                if field in keys:
                    encrypted_data = row[field]
                    if encrypted_data.startswith(version + ":"):
                        encrypted_data = encrypted_data[len(version) + 1 :]
                        row[field] = decrypt_data(keys[field], encrypted_data)
            writer.writerow(row)
