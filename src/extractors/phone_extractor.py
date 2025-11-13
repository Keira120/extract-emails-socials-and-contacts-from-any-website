thonimport re
from typing import Iterable, List, Set

PHONE_REGEX = re.compile(
    r"""
    (?<!\d)                       # no digit before
    (\+?\d{1,3}[\s.-]?)?          # optional country code
    (?:\(?\d{2,4}\)?[\s.-]?)?     # optional area code
    \d{3,4}[\s.-]?\d{3,4}         # local number
    (?!\d)                        # no digit after
    """,
    re.VERBOSE,
)

def extract_phone_numbers(text: str) -> List[str]:
    numbers: Set[str] = set()
    for match in PHONE_REGEX.finditer(text or ""):
        raw = match.group(0)
        cleaned = " ".join(raw.split())
        # Heuristic length filter to avoid junk
        digits = [c for c in cleaned if c.isdigit()]
        if len(digits) < 7:
            continue
        numbers.add(cleaned)
    return sorted(numbers)

def merge_phone_lists(*lists: Iterable[str]) -> List[str]:
    combined: Set[str] = set()
    for lst in lists:
        for phone in lst:
            combined.add(phone.strip())
    return sorted(combined)