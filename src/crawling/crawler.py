thonfrom collections import deque
from dataclasses import dataclass
import logging
from typing import Dict, List, Set, Tuple

from bs4 import BeautifulSoup

from src.crawling.js_renderer import JSRenderer
from src.crawling.page_queue import PageQueue
from src.extractors.email_extractor import extract_emails_from_text, merge_email_lists
from src.extractors.phone_extractor import extract_phone_numbers, merge_phone_lists
from src.extractors.social_extractor import extract_social_links
from src.utils.html_utils import (
    extract_links,
    find_contact_like_links,
    get_page_text,
    get_soup,
)
from src.utils.logging_utils import get_logger
from src.utils.url_utils import is_http_url, is_same_domain, normalize_url

@dataclass
class CrawlerConfig:
    max_pages_per_site: int = 30
    max_depth: int = 3
    request_timeout: int = 20
    user_agent: str = "BitbashContactScraper/1.0"

class WebsiteCrawler:
    """
    Website crawler that discovers emails, social links and phone numbers.

    It prioritizes contact-like pages (Contact, About, Team, Support) but will
    fall back to general internal links up to the configured depth and page limit.
    """

    def __init__(
        self,
        config: CrawlerConfig | None = None,
        logger: logging.Logger | None = None,
        renderer: JSRenderer | None = None,
    ) -> None:
        self.config = config or CrawlerConfig()
        self.logger = logger or get_logger("website_crawler")
        self.renderer = renderer or JSRenderer(
            user_agent=self.config.user_agent,
            timeout=self.config.request_timeout,
        )

    def _fetch_url(self, url: str) -> str:
        self.logger.debug("Fetching URL: %s", url)
        return self.renderer.fetch(url)

    def _extract_new_links(
        self, soup: BeautifulSoup, base_url: str
    ) -> Tuple[List[str], List[str]]:
        all_links = extract_links(soup, base_url)
        contact_like = find_contact_like_links(soup, base_url)
        contact_set = set(contact_like)
        general_links = [u for u in all_links if u not in contact_set]
        return contact_like, general_links

    def crawl(self, url: str) -> Dict:
        root_url = normalize_url(url)
        queue = PageQueue()
        queue.push(root_url, depth=0)
        scanned_pages: List[str] = []
        all_emails: List[str] = []
        all_phones: List[str] = []
        social_links_agg: Dict[str, List[str]] = {}
        status = "success"
        error_message = None

        pages_processed = 0

        while len(queue) and pages_processed < self.config.max_pages_per_site:
            item = queue.pop()
            if item is None:
                break
            current_url, depth = item
            if depth > self.config.max_depth:
                continue

            try:
                html = self._fetch_url(current_url)
                soup = get_soup(html)
            except Exception as exc:
                self.logger.warning("Failed to fetch %s: %s", current_url, exc)
                if not scanned_pages:
                    status = "error"
                    error_message = str(exc)
                continue

            scanned_pages.append(current_url)
            pages_processed += 1

            text = get_page_text(soup)
            emails = extract_emails_from_text(text)
            phones = extract_phone_numbers(text)
            all_emails = merge_email_lists(all_emails, emails)
            all_phones = merge_phone_lists(all_phones, phones)

            socials = extract_social_links(soup, current_url)
            for platform, links in socials.items():
                social_links_agg.setdefault(platform, [])
                for link in links:
                    if link not in social_links_agg[platform]:
                        social_links_agg[platform].append(link)

            contact_links, general_links = self._extract_new_links(soup, current_url)

            next_depth = depth + 1
            prioritized = [
                u for u in contact_links if is_same_domain(root_url, u) and is_http_url(u)
            ]
            general = [
                u for u in general_links if is_same_domain(root_url, u) and is_http_url(u)
            ]

            for u in prioritized:
                queue.push(u, next_depth)
            for u in general:
                queue.push(u, next_depth)

        record = {
            "url": root_url,
            "emails": all_emails,
            "social_links": social_links_agg,
            "phone_numbers": all_phones,
            "scanned_pages": scanned_pages,
            "status": status,
            "error": error_message,
        }
        return record