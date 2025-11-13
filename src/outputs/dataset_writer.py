thonimport csv
import json
import os
from typing import Any, Dict, Iterable, List

from src.outputs.export_formats import ExportFormat
from src.utils.logging_utils import get_logger
from src.utils.validation_utils import validate_output_record

class DatasetWriter:
    def __init__(self, logger=None) -> None:
        self.logger = logger or get_logger("dataset_writer")

    def _ensure_parent_dir(self, path: str) -> None:
        parent = os.path.dirname(path)
        if parent and not os.path.exists(parent):
            os.makedirs(parent, exist_ok=True)

    def _write_json(self, records: List[Dict[str, Any]], path: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2, ensure_ascii=False)

    def _write_ndjson(self, records: List[Dict[str, Any]], path: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            for rec in records:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    def _flatten_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        flat: Dict[str, Any] = {
            "url": record.get("url"),
            "status": record.get("status"),
            "error": record.get("error"),
            "emails": ";".join(record.get("emails") or []),
            "phone_numbers": ";".join(record.get("phone_numbers") or []),
            "scanned_pages": ";".join(record.get("scanned_pages") or []),
        }

        social_links = record.get("social_links") or {}
        for platform, links in social_links.items():
            flat[f"social_{platform}"] = ";".join(links)
        return flat

    def _write_csv(self, records: List[Dict[str, Any]], path: str) -> None:
        flattened = [self._flatten_record(r) for r in records]
        fieldnames: List[str] = sorted(
            {k for rec in flattened for k in rec.keys()}
        )
        with open(path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for rec in flattened:
                writer.writerow(rec)

    def write(
        self,
        records: List[Dict[str, Any]],
        fmt: str,
        path: str,
    ) -> None:
        export_format = ExportFormat.from_string(fmt)
        for rec in records:
            validate_output_record(rec)

        self._ensure_parent_dir(path)
        self.logger.info("Writing %d records as %s to %s", len(records), export_format, path)

        if export_format is ExportFormat.JSON:
            self._write_json(records, path)
        elif export_format is ExportFormat.NDJSON:
            self._write_ndjson(records, path)
        elif export_format is ExportFormat.CSV:
            self._write_csv(records, path)
        else:  # pragma: no cover - safeguarded by ExportFormat
            raise ValueError(f"Unsupported export format: {export_format}")