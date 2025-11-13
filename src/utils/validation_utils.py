thonfrom typing import Any, Dict, List

REQUIRED_FIELDS = {
    "url": str,
    "emails": list,
    "social_links": dict,
    "phone_numbers": list,
    "scanned_pages": list,
    "status": str,
    "error": (str, type(None)),
}

def validate_output_record(record: Dict[str, Any]) -> None:
    for field, expected_type in REQUIRED_FIELDS.items():
        if field not in record:
            raise ValueError(f"Missing required field in record: {field}")
        value = record[field]
        if isinstance(expected_type, tuple):
            if not isinstance(value, expected_type):
                raise TypeError(
                    f"Field '{field}' has wrong type: {type(value).__name__}, "
                    f"expected {', '.join(t.__name__ for t in expected_type)}"
                )
        else:
            if not isinstance(value, expected_type):
                raise TypeError(
                    f"Field '{field}' has wrong type: {type(value).__name__}, expected {expected_type.__name__}"
                )

    if not isinstance(record["emails"], list) or any(
        not isinstance(e, str) for e in record["emails"]
    ):
        raise TypeError("Field 'emails' must be a list of strings.")
    if not isinstance(record["phone_numbers"], list) or any(
        not isinstance(p, str) for p in record["phone_numbers"]
    ):
        raise TypeError("Field 'phone_numbers' must be a list of strings.")
    if not isinstance(record["scanned_pages"], list) or any(
        not isinstance(u, str) for u in record["scanned_pages"]
    ):
        raise TypeError("Field 'scanned_pages' must be a list of strings.")