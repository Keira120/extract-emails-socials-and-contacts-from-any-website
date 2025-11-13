thonfrom typing import Optional

import requests

from src.utils.logging_utils import get_logger

class JSRenderer:
    """
    Lightweight JS renderer. If `requests_html` is available, it will use it
    to execute JavaScript. Otherwise it falls back to plain HTTP GET requests.
    """

    def __init__(self, user_agent: str, timeout: int = 20) -> None:
        self.user_agent = user_agent
        self.timeout = timeout
        self.logger = get_logger("js_renderer")
        self._session = None
        try:
            from requests_html import HTMLSession  # type: ignore

            self._session = HTMLSession()
            self.logger.debug("Using requests_html for JS rendering.")
        except Exception:  # pragma: no cover - optional dependency
            self.logger.info(
                "requests_html not available; falling back to plain requests."
            )

    def fetch(self, url: str) -> str:
        headers = {"User-Agent": self.user_agent}
        if self._session is not None:
            resp = self._session.get(url, headers=headers, timeout=self.timeout)
            try:
                # Best-effort JS rendering; ignore errors.
                resp.html.render(timeout=self.timeout)  # type: ignore[attr-defined]
            except Exception:  # pragma: no cover - depends on external browser
                self.logger.debug("JS rendering failed for %s, using raw HTML.", url)
            resp.raise_for_status()
            return resp.text

        resp = requests.get(url, headers=headers, timeout=self.timeout)
        resp.raise_for_status()
        return resp.text