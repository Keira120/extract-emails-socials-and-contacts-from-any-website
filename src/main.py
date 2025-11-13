thonimport argparse
import json
import os
import sys
from typing import Any, Dict, List

from src.config.settings import load_settings, Settings
from src.crawling.crawler import CrawlerConfig, WebsiteCrawler
from src.outputs.dataset_writer import DatasetWriter
from src.utils.logging_utils import get_logger

def _load_input(path: str) -> List[str]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Input file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    urls = data.get("urls")
    if not isinstance(urls, list):
        raise ValueError("Input JSON must contain a list field 'urls'.")
    return [u for u in urls if isinstance(u, str) and u.strip()]

def _build_crawler(settings: Settings):
    crawl_cfg = settings.crawl
    config = CrawlerConfig(
        max_pages_per_site=crawl_cfg.max_pages_per_site,
        max_depth=crawl_cfg.max_depth,
        request_timeout=crawl_cfg.request_timeout,
        user_agent=crawl_cfg.user_agent,
    )
    logger = get_logger("contact_scraper")
    return WebsiteCrawler(config=config, logger=logger), logger

def run(
    input_path: str,
    output_path: str,
    output_format: str | None = None,
    settings_path: str | None = None,
) -> None:
    settings = load_settings(settings_path)
    if output_format is not None:
        settings.output_format = output_format

    crawler, logger = _build_crawler(settings)
    urls = _load_input(input_path)

    logger.info("Starting contact scraping for %d URLs", len(urls))
    results: List[Dict[str, Any]] = []
    for url in urls:
        logger.info("Processing URL: %s", url)
        try:
            record = crawler.crawl(url)
        except Exception as exc:  # pragma: no cover - defensive
            logger.exception("Failed to process URL %s", url)
            record = {
                "url": url,
                "emails": [],
                "social_links": {},
                "phone_numbers": [],
                "scanned_pages": [],
                "status": "error",
                "error": str(exc),
            }
        results.append(record)

    writer = DatasetWriter(logger=logger)
    writer.write(results, settings.output_format, output_path)
    logger.info("Finished writing dataset to %s (%s records)", output_path, len(results))

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract emails, social links and phone numbers from websites."
    )
    parser.add_argument(
        "--input",
        "-i",
        default="data/input.example.json",
        help="Path to input JSON file containing 'urls' list (default: data/input.example.json).",
    )
    parser.add_argument(
        "--output",
        "-o",
        default="data/sample_output.json",
        help="Path to output dataset file (default: data/sample_output.json).",
    )
    parser.add_argument(
        "--format",
        "-f",
        choices=["json", "csv", "ndjson"],
        help="Output format: json, csv or ndjson (default from settings).",
    )
    parser.add_argument(
        "--settings",
        "-s",
        help="Optional path to settings JSON file (overrides settings.example.json).",
    )
    args = parser.parse_args()

    run(
        input_path=args.input,
        output_path=args.output,
        output_format=args.format,
        settings_path=args.settings,
    )

if __name__ == "__main__":
    # Ensure project root is on sys.path for direct execution
    ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    if ROOT_DIR not in sys.path:
        sys.path.insert(0, ROOT_DIR)
    main()