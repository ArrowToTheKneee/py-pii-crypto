import typer

from piicrypto.encrypt_decrypt.decryptor import decrypt_csv_file, decrypt_data
from piicrypto.encrypt_decrypt.encryptor import encrypt_csv_file, encrypt_data
from piicrypto.key_provider.key_manager import KeyManager

app = typer.Typer()
keys_app = typer.Typer()
app.add_typer(keys_app, name="keys")
csv_app = typer.Typer()
app.add_typer(csv_app, name="csv")
data_app = typer.Typer()
app.add_typer(data_app, name="data")


@keys_app.command("generate")
def generate_keys_command(
    config_file: str = typer.Option(..., help="Path to key provider config JSON file."),
    mode: str = typer.Option(..., help="Key provider mode: 'local', 'vault', etc"),
):
    """
    Generate AES keys for the specified fields and save them to a JSON file.
    """
    key_manager = KeyManager(mode, config_file)
    key_manager.generate_keys()


@keys_app.command("rotate")
def rotate_keys_command(
    config_file: str = typer.Option(..., help="Path to key provider config JSON file."),
    mode: str = typer.Option(..., help="Key provider mode: 'local', 'vault', etc"),
):
    """
    Rotate AES keys in the specified JSON file.
    """
    key_manager = KeyManager(mode, config_file)
    key_manager.generate_keys()


@data_app.command("encrypt")
def encrypt_data_command(
    key: str = typer.Option(..., help="Base64-encoded AES key for encryption."),
    data: str = typer.Option(..., help="Data to encrypt."),
    nonce: str = typer.Option(..., help="Base64-encoded nonce used for encryption."),
):
    """
    Encrypt data using AES encryption.
    """
    encrypt_data(key, data, nonce)


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
    config_file: str = typer.Option(..., help="Path to key provider config JSON file."),
    mode: str = typer.Option(..., help="Key provider mode: 'local', 'vault', etc"),
    aliases_file: str = typer.Option(
        None, help="Path to the JSON file containing field aliases."
    ),
):
    """
    Encrypt specified fields in a CSV file using AES encryption.
    """
    key_manager = KeyManager(mode, config_file)
    encrypt_csv_file(input_file, output_file, key_manager, aliases_file)


@csv_app.command("decrypt")
def decrypt_csv_command(
    input_file: str = typer.Option(..., help="Path to the input CSV file."),
    output_file: str = typer.Option(..., help="Path to the output CSV file."),
    config_file: str = typer.Option(..., help="Path to key provider config JSON file."),
    mode: str = typer.Option(..., help="Key provider mode: 'local', 'vault', etc"),
    aliases_file: str = typer.Option(
        None, help="Path to the JSON file containing field aliases."
    ),
):
    """
    Decrypt specified fields in a CSV file using AES decryption.
    """
    key_manager = KeyManager(mode, config_file)
    decrypt_csv_file(input_file, output_file, key_manager, aliases_file)


if __name__ == "__main__":
    app()
