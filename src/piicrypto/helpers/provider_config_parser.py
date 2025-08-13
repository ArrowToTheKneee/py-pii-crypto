import json
from dataclasses import dataclass
from typing import Any, Dict, Optional

from piicrypto.helpers.logger_helper import setup_logger

logger = setup_logger(name=__name__)


@dataclass
class FieldConfig:
    """
    Represents the structure of each field in the provider configuration.
    """

    field: str
    alias: Optional[str] = None
    encrypt: bool = True
    key_id: Optional[str] = None

    def __post__init__(self):
        self.alias = self.alias or self.field


class ProviderConfigParser:
    """
    Parses the provider config from a JSON file and provides access to field configurations.
    """

    def __init__(self, config_file: str):
        """
        Initialize the parser with the path to the config file.
        """
        self.config_file = config_file
        self.fields: Dict[str, FieldConfig] = {}
        self.raw_config = self.load_config()
        self.key_source = self.raw_config.get("key_source", None)
        self.vault_url = self.raw_config.get("vault_url", None)
        if not self.key_source and not self.vault_url:
            logger.error("Configuratio file must contain 'key_source' or 'vault_url'.")
            raise ValueError(
                "Configuration file must contain 'key_source' or 'vault_url'."
            )
        logger.info(f"Loaded provider config from {self.config_file}")
        self.parse_fields()

    def load_config(self) -> Dict[str, Any]:
        """
        Load the JSON configuration file.
        """

        try:
            with open(self.config_file, "r") as f:
                return json.load(f)
        except FileNotFoundError as e:
            logger.error(f"Configuration file {self.config_file} not found.")
            raise FileNotFoundError(
                f"Configuration file {self.config_file} not found."
            ) from e
        except json.JSONDecodeError as e:
            logger.error(
                f"Configuration file {self.config_file} contains invalid JSON."
            )
            raise ValueError(
                f"Configuration file {self.config_file} contains invalid JSON."
            ) from e
        except Exception as e:
            logger.error(f"An error occurred while loading the configuration: {e}")
            raise RuntimeError(
                f"An error occurred while loading the configuration: {e}"
            )

    def parse_fields(self):
        """
        Parse the fields from the loaded configuration.
        """
        fields_config = self.raw_config.get("fields", {})
        for field, config in fields_config.items():
            if not isinstance(config, dict):
                logger.error(f"Field '{field}' configuration must be a dictionary.")
                raise ValueError(f"Field '{field}' configuration must be a dictionary.")
            alias = config.get("alias", field)
            encrypt = config.get("encrypt", True)
            key_id = config.get("key_id")
            self.fields[field] = FieldConfig(
                field=field, alias=alias, encrypt=encrypt, key_id=key_id
            )

    def get_field_to_alias(self) -> Dict[str, str]:
        """
        Get a mapping of field names to their aliases.
        """
        return {field: config.alias for field, config in self.fields.items()}

    def get_fields_to_encrypt(self) -> list:
        """
        Get a dictionary of fields that are marked for encryption.
        """
        return [field for field, config in self.fields.items() if config.encrypt]

    def get_fields_to_key_ids(self) -> Dict[str, str]:
        """
        Get a mapping of field names to their key IDs.
        """
        return {
            field: config.key_id
            for field, config in self.fields.items()
            if config.key_id and config.encrypt
        }
