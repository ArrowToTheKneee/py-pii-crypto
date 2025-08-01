import json
import os
from collections import defaultdict

from piicrypto.helpers.logger_helper import setup_logger
from piicrypto.helpers.utils import generate_aes_key
from piicrypto.key_provider.base_key_provider import BaseKeyProvider

logger = setup_logger(name=__name__)


class LocalKeyProvider(BaseKeyProvider):
    """
    Local key provider that generates and manages AES keys.
    This provider generates keys for specified fields and saves them to a JSON file.
    """

    def __init__(self, config_file: str):
        """
        Initialize the LocalKeyProvider from a config file.

        :param config_file: Path to a JSON config file with keys like:
            {
                "fields": "name,email,ssn",
                "json_file": "keys.json"
            }
        """
        with open(config_file, "r") as f:
            config = json.load(f)

        self.fields = config.get("fields", "")
        self.json_file = config.get("json_file", "keys.json")
        if not os.path.exists(self.json_file):
            logger.info(
                f"[LocalKeyProvider] Key file '{self.json_file}' does not exist. Generating keys."
            )
            self.generate_keys()
        else:
            logger.info(
                f"[LocalKeyProvider] Key file '{self.json_file}' already exists. Using existing keys."
            )

    def _load_keys_file(self):
        try:
            with open(self.json_file, "r") as f:
                return json.load(f)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Key file {self.json_file} not found.") from e
        except json.JSONDecodeError as e:
            raise ValueError(f"Key file {self.json_file} contains invalid JSON.") from e
        except Exception as e:
            raise RuntimeError(f"An error occurred while loading keys: {e}")

    def generate_keys(self):
        """
        Generate AES keys for the specified fields and save them to a JSON file.
        """
        fields_list = self.fields.split(",")
        keys = defaultdict(dict)
        logger.info(f"Generating keys for fields: {fields_list}")
        for field in fields_list:
            keys["v1"][field] = generate_aes_key()
        with open(self.json_file, "w") as f:
            json.dump(keys, f, indent=4)

    def rotate_keys(self):
        """
        Rotate AES keys in the specified JSON file.
        """
        keys = self._load_keys_file()
        max_version = max(int(k[1:]) for k in keys.keys())
        new_version = f"v{max_version + 1}"
        keys[new_version] = {
            field: generate_aes_key() for field in keys[f"v{max_version}"]
        }

        with open(self.json_file, "w") as f:
            json.dump(keys, f, indent=4)
        logger.info(f"Rotated keys to version {new_version}")

    def load_latest_keys(self):
        """
        Load the latest version of keys from the JSON file.
        """
        keys = self._load_keys_file()
        max_version = max(int(k[1:]) for k in keys)
        return f"v{max_version}", keys[f"v{max_version}"]

    def get_keys_by_version(self, version: str):
        """
        Load AES keys for a specific version from the JSON file.
        """
        keys = self._load_keys_file()
        if version not in keys:
            raise ValueError(f"Version {version} not found in {self.json_file}")
        return keys[version]
