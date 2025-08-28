import pytest

from piicrypto.encrypt_decrypt.decryptor import decrypt_csv_file
from piicrypto.encrypt_decrypt.encryptor import encrypt_csv_file


def test_roundtrip_csv(tmp_path, sample_csv, provider_config):
    enc = tmp_path / "out.enc.csv"
    dec = tmp_path / "out.dec.csv"

    encrypt_csv_file(
        input_file=str(sample_csv),
        output_file=str(enc),
        mode="local",
        key_provider_config=str(provider_config),
        create_metadata=True,
        validate_json=None,
    )
    enc_text = enc.read_text()
    assert "row_iv" in enc_text
    assert ":" in enc_text.splitlines()[1].split(",")[2]

    decrypt_csv_file(
        input_file=str(enc),
        output_file=str(dec),
        mode="local",
        key_provider_config=str(provider_config),
        create_metadata=True,
    )
    dec_text = dec.read_text()
    assert "Ada Lovelace" in dec_text
    assert "Alan Turing" in dec_text
