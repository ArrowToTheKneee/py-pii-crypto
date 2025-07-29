import base64
import csv

import typer
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

from key_manager import load_keys


def encrypt_data(key: str, data: str) -> str:
    """
    Encrypt data using AES encryption for the specified field.
    """
    key = base64.b64decode(key.encode())
    nonce = get_random_bytes(12)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(data.encode())
    combined = base64.b64encode(nonce + tag + ciphertext).decode()
    return combined


def encrypt_csv_file(input_file: str, output_file: str, keys_file: str):
    """
    Encrypt specified fields in a CSV file using AES encryption.
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
                    row[field] = f"{version}:" + encrypt_data(keys[field], row[field])
            writer.writerow(row)
