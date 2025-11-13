thonfrom urllib.parse import urljoin, urlparse, urlunparse

def normalize_url(url: str) -> str:
    url = url.strip()
    if not url:
        return url
    parsed = urlparse(url, scheme="http")
    scheme = parsed.scheme or "http"
    netloc = parsed.netloc or parsed.path
    path = "" if parsed.netloc else ""
    normalized = urlunparse((scheme, netloc, path, "", "", ""))
    return normalized.rstrip("/")

def make_absolute_url(base_url: str, href: str) -> str:
    return urljoin(base_url, href)

def is_http_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme in ("http", "https")

def _normalize_host(host: str) -> str:
    host = host.lower()
    if host.startswith("www."):
        return host[4:]
    return host

def is_same_domain(url_a: str, url_b: str) -> bool:
    pa = urlparse(url_a)
    pb = urlparse(url_b)
    if not pa.netloc or not pb.netloc:
        return False
    return _normalize_host(pa.netloc) == _normalize_host(pb.netloc)