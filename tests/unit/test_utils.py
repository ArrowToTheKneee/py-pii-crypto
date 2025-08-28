import piicrypto.helpers.utils as utils


def test_skip_id_column_by_name_and_sequence():
    assert utils.skip_id_column(1, "1", "id")
    assert utils.skip_id_column(5, "5", "row_number")
    assert not utils.skip_id_column(3, "42", "Name")


def test_find_best_match_prefers_alias_list():
    mapping = {"ssn": ["SSN", "Social Security Number"]}
    assert utils.find_best_match("SSN", mapping) == "ssn"
