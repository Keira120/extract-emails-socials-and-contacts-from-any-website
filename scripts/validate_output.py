thonimport json
import os
import sys

from src.utils.logging_utils import get_logger
from src.utils.validation_utils import validate_output_record

def main() -> None:
    logger = get_logger("validate_output")
    if len(sys.argv) < 2:
        logger.error("Usage: validate_output.py <path-to-output-json-or-ndjson>")
        sys.exit(1)

    path = sys.argv[1]
    if not os.path.exists(path):
        logger.error("File not found: %s", path)
        sys.exit(1)

    records = []
    if path.endswith(".ndjson"):
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                records.append(json.loads(line))
    else:
        with open(path, "r", encoding="utf-8") as f:
            records = json.load(f)

    logger.info("Validating %d records from %s", len(records), path)
    for idx, rec in enumerate(records):
        try:
            validate_output_record(rec)
        except Exception as exc:  # pragma: no cover - defensive path
            logger.error("Record %d is invalid: %s", idx, exc)
            sys.exit(1)

    logger.info("All records are valid.")

if __name__ == "__main__":
    main()