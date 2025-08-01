from piicrypto.key_provider.base_key_provider import BaseKeyProvider
from piicrypto.key_provider.key_provider_factory import KeyProviderFactory


class KeyManager:
    """
    Facade for interacting with any key provider implementation.
    """

    def __init__(self, provider_type: str, config_file: str):
        """
        Initialize the KeyManager with a specified provider type and arguments.
        :param provider_type: 'local' or 'vault'
        param config_file: Path to a JSON config file with provider configuration.
        """
        self.provider: BaseKeyProvider = KeyProviderFactory.create_key_provider(
            provider_type, config_file
        )

    def generate_keys(self):
        """
        Generate new keys using the underlying provider.
        """
        self.provider.generate_keys()

    def rotate_keys(self):
        """
        Rotate keys using the underlying provider.
        """
        self.provider.rotate_keys()

    def load_latest_keys(self):
        """
        Load the latest version of keys from the provider.
        :return: (version_str, keys_dict)
        """
        return self.provider.load_latest_keys()

    def get_keys_by_version(self, version: str):
        """
        Get keys by version.
        :param version: The version to load (e.g., 'v1')
        :return: keys_dict
        """
        return self.provider.get_keys_by_version(version)
