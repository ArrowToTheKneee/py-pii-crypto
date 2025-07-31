import base64
import json
from collections import defaultdict

from Crypto.Random import get_random_bytes


def generate_aes_key():
    key_bytes = get_random_bytes(32)
    return base64.b64encode(key_bytes).decode()


def generate_keys(fields: str, json_file: str):
    """
    Generate AES keys for the specified fields and save them to a JSON file.
    """
    fields_list = fields.split(",")
    keys = defaultdict(dict)
    print(f"Generating keys for fields: {fields_list}")
    for field in fields_list:
        keys["v1"][field] = generate_aes_key()
    with open(json_file, "w") as f:
        json.dump(keys, f, indent=4)


def rotate_keys(json_file: str):
    """
    Rotate AES keys in the specified JSON file.
    """
    try:
        with open(json_file, "r+") as f:
            keys = json.load(f)
            max_version = max(int(k[1:]) for k in keys.keys())
            print(f"Rotating keys from v{max_version} to v{max_version + 1}")
            new_version = f"v{max_version + 1}"
            keys[new_version] = {}
            for field in keys[f"v{max_version}"].keys():
                keys[new_version][field] = generate_aes_key()
            f.seek(0)
            json.dump(keys, f, indent=4)
            f.truncate()
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: The file {json_file} does not exist.")
    except json.JSONDecodeError:
        raise json.JSONDecodeError(f"Error: The file {json_file} is not a valid JSON.")
    except Exception as e:
        raise RuntimeError(f"Error: {e}")


def load_latest_keys(json_file: str):
    """
    Load AES keys from a JSON file.
    """
    try:
        with open(json_file, "r") as f:
            keys = json.load(f)
        max_version = max(int(k[1:]) for k in keys.keys())
        return f"v{max_version}", keys[f"v{max_version}"]
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: The file {json_file} does not exist.")
    except json.JSONDecodeError:
        raise json.JSONDecodeError(f"Error: The file {json_file} is not a valid JSON.")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {e}")


def get_keys_by_version(json_file: str, version: str):
    """
    Load AES keys for a specific version from a JSON file.
    """
    try:
        with open(json_file, "r") as f:
            keys = json.load(f)
        if version in keys:
            return keys[version]
        else:
            raise ValueError(f"Version {version} not found in the keys file.")
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: The file {json_file} does not exist.")
    except json.JSONDecodeError:
        raise json.JSONDecodeError(f"Error: The file {json_file} is not a valid JSON.")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {e}")
