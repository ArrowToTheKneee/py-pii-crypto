from abc import ABC, abstractmethod


class BaseKeyProvider(ABC):
    """
    Abstract base class for key providers.
    All key providers should inherit from this class and implement the required methods.
    """

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
    def load_latest_keys(self):
        """
        Load latest AES keys from a JSON file.
        """
        pass

    @abstractmethod
    def get_keys_by_version(self, version: str):
        """
        Load AES keys for a specific version from a JSON file.
        """
        pass
