thonimport json
import os
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class CrawlSettings:
    max_pages_per_site: int = 30
    max_depth: int = 3
    concurrency: int = 5
    request_timeout: int = 20
    user_agent: str = "BitbashContactScraper/1.0"

@dataclass
class EmailFilterSettings:
    blocked_patterns: List[str] = field(
        default_factory=lambda: [
            "noreply@",
            "no-reply@",
            "do-not-reply@",
            "donotreply@",
        ]
    )
    blocked_domains: List[str] = field(default_factory=list)
    allowed_domains: List[str] = field(default_factory=list)

@dataclass
class Settings:
    crawl: CrawlSettings = field(default_factory=CrawlSettings)
    email_filters: EmailFilterSettings = field(default_factory=EmailFilterSettings)
    output_format: str = "json"

def _update_dataclass_from_dict(instance, data: dict) -> None:
    for key, value in data.items():
        if hasattr(instance, key):
            attr = getattr(instance, key)
            if hasattr(attr, "__dataclass_fields__") and isinstance(value, dict):
                _update_dataclass_from_dict(attr, value)
            else:
                setattr(instance, key, value)

def _load_json_if_exists(path: str) -> Optional[dict]:
    if not path:
        return None
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_settings(path: Optional[str] = None) -> Settings:
    """
    Load settings from JSON file if present; otherwise return defaults.

    Resolution order:
    1. Explicit `path` argument.
    2. Environment variable SCRAPER_SETTINGS.
    3. src/config/settings.example.json (if present).
    """
    settings = Settings()
    config_path = (
        path
        or os.environ.get("SCRAPER_SETTINGS")
        or os.path.join(
            os.path.dirname(__file__),
            "settings.example.json",
        )
    )

    data = _load_json_if_exists(config_path)
    if data:
        _update_dataclass_from_dict(settings, data)
    return settings