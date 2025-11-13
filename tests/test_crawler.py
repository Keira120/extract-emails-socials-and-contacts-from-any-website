thonfrom src.crawling.crawler import CrawlerConfig, WebsiteCrawler

HTML_FIXTURE = """
<html>
  <body>
    <a href="mailto:info@example.com">Email</a>
    <a href="https://facebook.com/example">Facebook</a>
    <span>+1 (555) 123-4567</span>
    <a href="/contact">Contact</a>
  </body>
</html>
"""

def test_crawler_collects_basic_contact_data(monkeypatch):
    config = CrawlerConfig(
        max_pages_per_site=2,
        max_depth=1,
        request_timeout=5,
        user_agent="TestAgent/1.0",
    )
    crawler = WebsiteCrawler(config=config)

    # Avoid any real network calls by monkeypatching _fetch_url
    monkeypatch.setattr(crawler, "_fetch_url", lambda url: HTML_FIXTURE)

    record = crawler.crawl("https://example.com")

    assert record["url"].startswith("http")
    assert "info@example.com" in record["emails"]
    assert any("123-4567" in n for n in record["phone_numbers"])
    assert "facebook" in record["social_links"]
    assert record["status"] == "success"
    assert record["error"] is None
    assert len(record["scanned_pages"]) >= 1