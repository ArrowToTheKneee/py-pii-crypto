import base64

import pytest

from piicrypto.encrypt_decrypt.decryptor import decrypt_data
from piicrypto.encrypt_decrypt.encryptor import encrypt_data
from piicrypto.helpers.utils import generate_aes_key, generate_nonce


def test_encrypt_decrypt_data():
    original_data = "Sensitive Information"
    key = generate_aes_key()
    nonce = generate_nonce()

    encrypted_data = encrypt_data(key, original_data, nonce)

    assert encrypted_data != original_data, "Encrypted data should differ from original"
    assert len(encrypted_data) > 0, "Encrypted data should not be empty"

    decrypted_data = decrypt_data(key, encrypted_data, base64.b64encode(nonce).decode())

    assert decrypted_data == original_data, "Decrypted data should match the original"
