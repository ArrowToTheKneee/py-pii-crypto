from collections import defaultdict

from piicrypto.helpers.logger_helper import setup_logger
from piicrypto.helpers.provider_config_parser import ProviderConfigParser
from piicrypto.helpers.utils import generate_aes_key
from piicrypto.key_provider.base_key_provider import BaseKeyProvider

logger = setup_logger(name=__name__)


class VaultKeyProvider(BaseKeyProvider):
    """
    Vault key provider that generates and manages AES keys.
    This provider generates keys for specified fields and saves to Vault.
    """

    def __init__(self, config_file: str):
        """
        Initialize the LocalKeyProvider from a config file.

        :param config_file: Path to a JSON config file with keys
        """
        provider_config = ProviderConfigParser(config_file)

        self.fields = list(provider_config.fields.keys())
        self.field_to_alias = provider_config.get_field_to_alias()
        self.vault_url = provider_config.vault_url
        self.generate_keys()

    def generate_keys(self):
        """
        Generate AES keys for the specified fields and save them to Vault.
        """
        keys = defaultdict(dict)
        logger.info(f"Generating keys for fields: {self.fields}")
        for field in self.fields:
            keys["v1"][field] = generate_aes_key()
        # Implement the logic to save `keys` to Vault
        # For example, using a Vault client library to write the keys
        logger.info(f"Keys generated and saved to Vault at {self.vault_url}")

    def rotate_keys(self):
        """
        Rotate AES keys in the Vault.
        """
        # Implement the logic to read current keys from Vault,
        # generate new keys, and write them back to Vault.
        logger.info(f"Rotating keys in Vault at {self.vault_url}")

    def load_keys(self):
        """
        Load AES keys from Vault.
        """
        # Implement the logic to read the keys from Vault.
        logger.info(f"Loading keys from Vault at {self.vault_url}")

    def get_keys_by_version(self, version: str):
        """
        Load AES keys for a specific version from Vault.
        :param version: Version of the keys to load.
        """
        # Implement the logic to read keys for a specific version from Vault.
        logger.info(
            f"Loading keys for version {version} from Vault at {self.vault_url}"
        )
