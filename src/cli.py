import typer

from decryptor import decrypt_csv_file, decrypt_data
from encryptor import encrypt_csv_file, encrypt_data
from key_manager import generate_keys, rotate_keys

app = typer.Typer()


@app.command("generate-keys")
def generate_keys_command(
    fields: str = typer.Option(
        ..., help="Comma-separated list of fields to generate keys for."
    ),
    json_file: str = typer.Option(
        ..., help="Path to the JSON file to save the generated keys."
    ),
):
    """
    Generate AES keys for the specified fields and save them to a JSON file.
    """
    generate_keys(fields, json_file)


@app.command("rotate-keys")
def rotate_keys_command(
    json_file: str = typer.Option(
        ..., help="Path to the JSON file containing the keys."
    ),
):
    """
    Rotate AES keys in the specified JSON file.
    """
    rotate_keys(json_file)


@app.command("encrypt-data")
def encrypt_data_command(
    key: str = typer.Option(..., help="Base64-encoded AES key for encryption."),
    data: str = typer.Option(..., help="Data to encrypt."),
):
    """
    Encrypt data using AES encryption.
    """
    encrypt_data(key, data)


@app.command("decrypt-data")
def decrypt_data_command(
    key: str = typer.Option(..., help="Base64-encoded AES key for decryption."),
    data: str = typer.Option(..., help="Data to decrypt."),
):
    """
    Decrypt data using AES decryption.
    """
    decrypt_data(key, data)


@app.command("encrypt-csv")
def encrypt_csv_command(
    input_file: str = typer.Option(..., help="Path to the input CSV file."),
    output_file: str = typer.Option(..., help="Path to the output CSV file."),
    keys_file: str = typer.Option(
        ..., help="Path to the JSON file containing the keys."
    ),
):
    """
    Encrypt specified fields in a CSV file using AES encryption.
    """
    encrypt_csv_file(input_file, output_file, keys_file)


@app.command("decrypt-csv")
def decrypt_csv_command(
    input_file: str = typer.Option(..., help="Path to the input CSV file."),
    output_file: str = typer.Option(..., help="Path to the output CSV file."),
    keys_file: str = typer.Option(
        ..., help="Path to the JSON file containing the keys."
    ),
):
    """
    Decrypt specified fields in a CSV file using AES decryption.
    """
    decrypt_csv_file(input_file, output_file, keys_file)


if __name__ == "__main__":
    app()
