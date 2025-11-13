thonfrom typing import List
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from src.utils.url_utils import is_http_url, make_absolute_url

CONTACT_KEYWORDS = ("contact", "about", "team", "support", "help")

def get_soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html or "", "lxml")

def get_page_text(soup: BeautifulSoup) -> str:
    return " ".join(s for s in soup.stripped_strings)

def extract_links(soup: BeautifulSoup, base_url: str) -> List[str]:
    links: List[str] = []
    seen = set()
    for tag in soup.find_all("a", href=True):
        href = tag.get("href")
        if not href:
            continue
        absolute = make_absolute_url(base_url, href)
        if not is_http_url(absolute):
            continue
        if absolute in seen:
            continue
        seen.add(absolute)
        links.append(absolute)
    return links

def find_contact_like_links(soup: BeautifulSoup, base_url: str) -> List[str]:
    """
    Return URLs that look like "Contact", "About", "Team", "Support" pages.
    """
    contact_links: List[str] = []
    seen = set()
    for tag in soup.find_all("a", href=True):
        text = (tag.get_text() or "").strip().lower()
        href = tag.get("href")
        if not href:
            continue
        absolute = make_absolute_url(base_url, href)
        if not is_http_url(absolute):
            continue

        parsed = urlparse(absolute)
        path = parsed.path.lower()
        is_contact_like = any(k in text for k in CONTACT_KEYWORDS) or any(
            k in path for k in CONTACT_KEYWORDS
        )

        if is_contact_like and absolute not in seen:
            seen.add(absolute)
            contact_links.append(absolute)

    return contact_links