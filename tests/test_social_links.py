thonfrom bs4 import BeautifulSoup

from src.extractors.social_extractor import extract_social_links

def test_extract_social_links_detects_platforms():
    html = """
    <html><body>
        <a href="https://facebook.com/example">FB</a>
        <a href="https://twitter.com/example">TW</a>
        <a href="https://linkedin.com/company/example">IN</a>
    </body></html>
    """
    soup = BeautifulSoup(html, "lxml")
    links = extract_social_links(soup, "https://example.com")

    assert "facebook" in links
    assert "twitter" in links
    assert "linkedin" in links

    assert "https://facebook.com/example" in links["facebook"]
    assert "https://twitter.com/example" in links["twitter"]
    assert "https://linkedin.com/company/example" in links["linkedin"]