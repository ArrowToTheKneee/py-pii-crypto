import json

from Crypto.Random import get_random_bytes
from rapidfuzz import fuzz, utils
from rapidfuzz.process import extractOne


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
    print(f"Best match for '{query}': '{match}' with similarity {similarity}")
    return reverse_lookup[match] if similarity >= 95 else query
