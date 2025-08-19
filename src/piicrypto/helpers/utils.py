import base64
from datetime import datetime
from importlib.metadata import version

from Crypto.Random import get_random_bytes
from pydantic import BaseModel, ValidationError
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


def find_best_match(query: str, field_to_alias: dict) -> str:
    """
    Find the best match for a query string in a field to alias dict using fuzzy matching.
    """
    reverse_lookup = {v: k for k, vs in field_to_alias.items() for v in vs}
    match, similarity, _ = extractOne(
        query,
        list(reverse_lookup.keys()),
        scorer=fuzz.token_set_ratio,
        processor=utils.default_process,
    )
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


def generate_metadata(
    out_file: str, mode: str, operation: str, operation_fields: set
) -> dict:
    """
    Generate metadata for the keys.
    """
    metadata = {
        "key_provider_mode": mode,
        "operation": operation,
        "operation_fields": list(operation_fields),
        "output_file": out_file,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "package_version": version("pii-crypto"),
    }
    return metadata


def validate_row(row: dict, model: BaseModel) -> bool:
    """
    Validate a row against the dynamically created Pydantic model.
    """
    try:
        model(**row)
        return True
    except ValidationError as e:
        error = e.errors()
        if error:
            for err in error:
                logger.error(
                    f"Validation error for field '{err['loc'][0]}': {err['msg']}"
                )
        else:
            logger.error(f"Validation error for row {row}: {e}")
        return False
