thonimport re
from typing import Iterable, List, Optional, Sequence, Set

EMAIL_REGEX = re.compile(
    r"(?i)(?P<email>[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,})"
)

def is_valid_email(
    email: str,
    blocked_patterns: Sequence[str] | None = None,
    blocked_domains: Sequence[str] | None = None,
    allowed_domains: Sequence[str] | None = None,
) -> bool:
    email = email.strip()
    if not email or "@" not in email:
        return False

    local, _, domain = email.rpartition("@")
    if not local or not domain:
        return False

    blocked_patterns = blocked_patterns or []
    blocked_domains = blocked_domains or []
    allowed_domains = allowed_domains or []

    lowered = email.lower()
    for pattern in blocked_patterns:
        if pattern.lower() in lowered:
            return False

    domain_lower = domain.lower()
    for blocked in blocked_domains:
        if domain_lower == blocked.lower():
            return False

    if allowed_domains:
        return any(domain_lower == d.lower() for d in allowed_domains)

    # simple heuristic to avoid obvious junk
    if ".." in email or email.endswith("."):
        return False
    return True

def extract_emails_from_text(
    text: str,
    blocked_patterns: Sequence[str] | None = None,
    blocked_domains: Sequence[str] | None = None,
    allowed_domains: Sequence[str] | None = None,
) -> List[str]:
    candidates: Set[str] = set()
    for match in EMAIL_REGEX.finditer(text or ""):
        email = match.group("email")
        if is_valid_email(
            email,
            blocked_patterns=blocked_patterns,
            blocked_domains=blocked_domains,
            allowed_domains=allowed_domains,
        ):
            candidates.add(email.strip())
    return sorted(candidates)

def merge_email_lists(*lists: Iterable[str]) -> List[str]:
    combined: Set[str] = set()
    for lst in lists:
        for email in lst:
            combined.add(email.strip())
    return sorted(combined)