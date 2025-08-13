from abc import ABC, abstractmethod

from piicrypto.helpers.provider_config_parser import ProviderConfigParser


class BaseKeyProvider(ABC):
    """
    Abstract base class for key providers.
    All key providers should inherit from this class and implement the required methods.
    """

    def __init__(self, config_file: str):
        provider_config = ProviderConfigParser(config_file)
        self.fields_to_encrypt = provider_config.get_fields_to_encrypt()
        self.field_to_alias = provider_config.get_field_to_alias()

    @abstractmethod
    def generate_keys(self):
        """
        Generate AES keys for the specified fields and save them to a JSON file.
        """
        pass

    @abstractmethod
    def rotate_keys(self):
        """
        Rotate AES keys in the specified JSON file.
        """
        pass

    @abstractmethod
    def load_keys(self):
        """
        Load AES keys from a JSON file.
        """
        pass

    @abstractmethod
    def get_keys_by_version(self, version: str):
        """
        Load AES keys for a specific version from a JSON file.
        """
        pass
