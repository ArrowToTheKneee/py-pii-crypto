import json
from datetime import datetime
from typing import Optional

from pydantic import Field, create_model, field_validator


def create_dynamic_model(config_json: str) -> type:
    """
    Create a dynamic Pydantic model based on the provided configuration dictionary.

    Args:
        config_json (str): A JSON string representing the configuration for the model.
        Eg:
            {
                "id": { "type": "int", "gt": 1, "required": True },
                "name": { "type": "str", "min_length": 1, "max_length": 50, "required": True },
                "Social Security Number": { "type": "str", "regex": "^[0-9]{3}-[0-9]{2}-[0-9]{4}$", "required": True },
                "address": { "type": "str", "min_length": 5, "max_length": 100, "required": True },
                "Date of Birth": { "type": "date", "format": "%Y-%m-%d", "required": True },
                "Country": { "type": "enum", "values": ["US", "CA", "UK"], "required": True }
            }

    Returns:
        type: A dynamically created Pydantic model class.
    """
    TYPE_MAPPING = {
        "int": int,
        "str": str,
        "date": str,
        "enum": str,
    }
    with open(config_json, "r") as file:
        config_dict = json.load(file)

    fields = {}
    validators = {}

    for field_name, field_config in config_dict.items():
        validation_rules = {}
        field_type = TYPE_MAPPING.get(field_config["type"], str)
        if not field_type:
            raise ValueError(
                f"Unsupported type: {field_config['type']} for field: {field_name}"
            )
        if field_config.get("required", True):
            default = ...
            annotated_type = field_type
        else:
            default = None
            annotated_type = Optional[field_type]
        if "gt" in field_config:
            validation_rules["gt"] = field_config["gt"]
        if "min_length" in field_config:
            validation_rules["min_length"] = field_config["min_length"]
        if "max_length" in field_config:
            validation_rules["max_length"] = field_config["max_length"]
        if "regex" in field_config:
            validation_rules["pattern"] = field_config["regex"]

        fields[field_name] = (annotated_type, Field(default, **validation_rules))

        def empty_to_none(v):
            if v == "":
                return None
            return v

        validators[f"empty_to_none_{field_name}"] = field_validator(
            field_name, mode="before"
        )(empty_to_none)

        if field_config["type"] == "date":
            fmt = field_config.get("format", "%Y-%m-%d")

            def _parse_date(v, fmt=fmt):
                try:
                    datetime.strptime(v, fmt).date()
                    return v
                except Exception:
                    raise ValueError(f"Expected date format {fmt}")

            validators[f"parse_date_{field_name}"] = field_validator(
                field_name, mode="after"
            )(_parse_date)

        if field_config["type"] == "enum":
            allowed = set(field_config.get("values", []))

            def _enum_validator(v, allowed=allowed):
                if v not in allowed:
                    raise ValueError(f"Value '{v}' not in allowed list: {allowed}")
                return v

            validators[f"_enum_validator_{field_name}"] = field_validator(
                field_name, mode="after"
            )(_enum_validator)

        # Not using Annotations like, fields[field_name] = Annotated[ field_type, *validators, Field(default, **validation_rules), ] due to error cannot use star expression in index

    model = create_model(
        "RowValidationModel", **fields, __pydantic_validator__=validators
    )
    return model
