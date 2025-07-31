import typer

from decryptor import decrypt_csv_file, decrypt_data
from encryptor import encrypt_csv_file, encrypt_data
from key_manager import generate_keys, rotate_keys

app = typer.Typer()
keys_app = typer.Typer()
app.add_typer(keys_app, name="keys")
csv_app = typer.Typer()
app.add_typer(csv_app, name="csv")
data_app = typer.Typer()
app.add_typer(csv_app, name="data")


@keys_app.command("generate")
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


@keys_app.command("rotate")
def rotate_keys_command(
    json_file: str = typer.Option(
        ..., help="Path to the JSON file containing the keys."
    ),
):
    """
    Rotate AES keys in the specified JSON file.
    """
    rotate_keys(json_file)


@data_app.command("decrypt")
def encrypt_data_command(
    key: str = typer.Option(..., help="Base64-encoded AES key for encryption."),
    data: str = typer.Option(..., help="Data to encrypt."),
    nonce: str = typer.Option(..., help="Base64-encoded nonce used for encryption."),
):
    """
    Encrypt data using AES encryption.
    """
    encrypt_data(key, data)


@data_app.command("decrypt")
def decrypt_data_command(
    key: str = typer.Option(..., help="Base64-encoded AES key for decryption."),
    data: str = typer.Option(..., help="Data to decrypt."),
    nonce: str = typer.Option(..., help="Base64-encoded nonce used for encryption."),
):
    """
    Decrypt data using AES decryption.
    """
    decrypt_data(key, data, nonce)


@csv_app.command("encrypt")
def encrypt_csv_command(
    input_file: str = typer.Option(..., help="Path to the input CSV file."),
    output_file: str = typer.Option(..., help="Path to the output CSV file."),
    keys_file: str = typer.Option(
        ..., help="Path to the JSON file containing the keys."
    ),
    aliases_file: str = typer.Option(
        None, help="Path to the JSON file containing field aliases."
    ),
):
    """
    Encrypt specified fields in a CSV file using AES encryption.
    """
    encrypt_csv_file(input_file, output_file, keys_file, aliases_file)


@csv_app.command("encrypt")
def decrypt_csv_command(
    input_file: str = typer.Option(..., help="Path to the input CSV file."),
    output_file: str = typer.Option(..., help="Path to the output CSV file."),
    keys_file: str = typer.Option(
        ..., help="Path to the JSON file containing the keys."
    ),
    aliases_file: str = typer.Option(
        None, help="Path to the JSON file containing field aliases."
    ),
):
    """
    Decrypt specified fields in a CSV file using AES decryption.
    """
    decrypt_csv_file(input_file, output_file, keys_file, aliases_file)


if __name__ == "__main__":
    app()
