import base64
import json

from Crypto.Random import get_random_bytes
from rapidfuzz import fuzz, utils
from rapidfuzz.process import extractOne

from piicrypto.helpers.logger_helper import setup_logger

logger = setup_logger(name=__name__)


def generate_aes_key():
    key_bytes = get_random_bytes(32)
    return base64.b64encode(key_bytes).decode()


def generate_nonce() -> bytes:
    """
    Generate a random nonce for AES encryption.
    """
    return get_random_bytes(12)


def find_best_match(query: str, aliases_file: str) -> str:
    """
    Find the best match for a query string in an aliases file using fuzzy matching.
    """
    with open(aliases_file, "r") as f:
        aliases = json.load(f)
    reverse_lookup = {v: k for k, vs in aliases.items() for v in vs}
    match, similarity, _ = extractOne(
        query,
        list(reverse_lookup.keys()),
        scorer=fuzz.token_set_ratio,
        processor=utils.default_process,
    )
    logger.info(f"Best match for '{query}': '{match}' with similarity {similarity}")
    return reverse_lookup[match] if similarity >= 95 else query


def skip_id_column(row_number: int, value: dict, field_name: str) -> bool:
    """
    Skip the ID column in the first row of a CSV file.
    """
    ROW_NUMBER_ALIASES = {"row_number", "id", "index", "sr_no", "s.no"}
    if field_name.lower() in ROW_NUMBER_ALIASES:
        return True
    stripped = value.strip()
    if stripped.isdigit() and int(stripped) == row_number:
        return True
    return False
