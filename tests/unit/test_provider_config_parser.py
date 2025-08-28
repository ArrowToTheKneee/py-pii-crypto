from piicrypto.helpers.provider_config_parser import ProviderConfigParser


def test_provider_config_parser(provider_config):
    parser = ProviderConfigParser(provider_config)
    assert parser.key_source is not None
    assert parser.vault_url is None
    assert "Social Security Number" in parser.fields
    ssn_field = parser.fields["Social Security Number"]
    assert ssn_field.alias == "ssn"
    assert ssn_field.encrypt is True
    assert ssn_field.key_id == "v1"

    name_field = parser.fields["Name"]
    assert name_field.alias == "name"
    assert name_field.encrypt is True
    assert name_field.key_id == "v1"

    address_field = parser.fields["Address"]
    assert address_field.alias == "address"
    assert address_field.encrypt is False
    assert address_field.key_id is None
