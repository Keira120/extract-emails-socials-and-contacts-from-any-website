thonfrom typing import Dict, List
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from src.utils.url_utils import make_absolute_url, is_http_url

SOCIAL_DOMAINS = {
    "facebook": ["facebook.com", "fb.me"],
    "twitter": ["twitter.com", "x.com"],
    "linkedin": ["linkedin.com"],
    "instagram": ["instagram.com"],
    "youtube": ["youtube.com", "youtu.be"],
    "tiktok": ["tiktok.com"],
    "pinterest": ["pinterest.com"],
    "snapchat": ["snapchat.com"],
    "telegram": ["t.me", "telegram.me"],
    "whatsapp": ["wa.me", "whatsapp.com"],
    "reddit": ["reddit.com"],
    "discord": ["discord.com", "discord.gg"],
    "medium": ["medium.com"],
    "behance": ["behance.net"],
    "dribbble": ["dribbble.com"],
    "github": ["github.com"],
    "gitlab": ["gitlab.com"],
    "vimeo": ["vimeo.com"],
    "twitch": ["twitch.tv"],
    "skype": ["skype.com"],
}

def _platform_for_url(href: str) -> str | None:
    try:
        parsed = urlparse(href)
    except ValueError:
        return None
    host = (parsed.netloc or "").lower()
    if not host:
        return None
    host = host.split(":")[0]
    for platform, domains in SOCIAL_DOMAINS.items():
        for d in domains:
            if host == d or host.endswith("." + d):
                return platform
    return None

def extract_social_links(soup: BeautifulSoup, base_url: str) -> Dict[str, List[str]]:
    social_links: Dict[str, List[str]] = {}
    for tag in soup.find_all("a", href=True):
        href = tag.get("href")
        if not href:
            continue
        absolute = make_absolute_url(base_url, href)
        if not is_http_url(absolute):
            continue
        platform = _platform_for_url(absolute)
        if not platform:
            continue
        social_links.setdefault(platform, [])
        if absolute not in social_links[platform]:
            social_links[platform].append(absolute)
    return social_links