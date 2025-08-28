import json

import pytest

from piicrypto.key_provider.key_manager import KeyManager


@pytest.fixture(scope="session")
def provider_config(tmp_path_factory):
    """
    Create a provider config JSON in a session-level temp directory.
    """
    base = tmp_path_factory.mktemp("provider")
    keys_path = base / "keys.json"
    cfg = {
        "key_source": str(keys_path),
        "fields": {
            "Social Security Number": {"alias": "ssn", "encrypt": True, "key_id": "v1"},
            "Name": {"alias": "name", "encrypt": True, "key_id": "v1"},
            "Address": {"alias": "address", "encrypt": False},
        },
    }
    p = base / "provider_config.json"
    with open(p, "w") as f:
        json.dump(cfg, f)

    yield str(p)

    # Cleanup
    if keys_path.exists():
        keys_path.unlink()
    if p.exists():
        p.unlink()
    if base.exists():
        base.rmdir()


@pytest.fixture
def key_manager(provider_config):
    """
    Instantiate the real KeyManager with the LocalKeyProvider.
    This will auto-generate v1 keys into the temp keys.json on first use.
    """
    km = KeyManager("local", str(provider_config))
    return km


@pytest.fixture
def validation_schema_json(tmp_path):
    schema = {
        "id": {"type": "int", "gt": 0, "required": True},
        "Name": {"type": "str", "min_length": 1, "required": True},
        "Social Security Number": {
            "type": "str",
            "regex": "^[0-9]{3}-[0-9]{2}-[0-9]{4}$",
            "required": True,
        },
        "Address": {"type": "str", "min_length": 3, "required": False},
    }
    p = tmp_path / "schema.json"
    p.write_text(json.dumps(schema, indent=2))
    return p


@pytest.fixture
def sample_csv(tmp_path):
    csv_text = (
        "id,Name,Social Security Number,Address\n"
        "1,Ada Lovelace,123-45-6789,London\n"
        "2,Alan Turing,111-22-3333,Manchester\n"
    )
    p = tmp_path / "in.csv"
    p.write_text(csv_text)
    return p
