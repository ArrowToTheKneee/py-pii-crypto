from piicrypto.key_provider.local_key_provider import LocalKeyProvider
from piicrypto.key_provider.vault_key_provider import VaultKeyProvider


class KeyProviderFactory:
    """
    Factory class to create key providers based on the type.
    """

    @staticmethod
    def create_key_provider(provider_type: str, config_file: str):
        """
        Create a key provider instance based on the provider type.
        :param provider_type: Type of the key provider ('local', 'vault', etc).
        :param config_file: Path to a JSON config file with provider configuration.
        :return: An instance of the specified key provider.
        """
        if provider_type == "local":
            return LocalKeyProvider(config_file)
        elif provider_type == "vault":
            return VaultKeyProvider(config_file)
        else:
            raise ValueError(f"Unknown key provider type: {provider_type}")
