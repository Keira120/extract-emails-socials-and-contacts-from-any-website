thonfrom enum import Enum

class ExportFormat(str, Enum):
    JSON = "json"
    CSV = "csv"
    NDJSON = "ndjson"

    @classmethod
    def from_string(cls, value: str) -> "ExportFormat":
        try:
            return cls(value.lower())
        except Exception as exc:
            raise ValueError(f"Unsupported export format: {value}") from exc