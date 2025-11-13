thonfrom src.extractors.email_extractor import extract_emails_from_text, is_valid_email

def test_is_valid_email_filters_blocked_patterns():
    assert is_valid_email("info@example.com", blocked_patterns=["noreply@"])
    assert not is_valid_email("noreply@example.com", blocked_patterns=["noreply@"])

def test_extract_emails_from_text_basic():
    text = """
    Contact us at info@example.com or support@example.com.
    This noreply@example.com should be ignored.
    """
    emails = extract_emails_from_text(text, blocked_patterns=["noreply@"])
    assert "info@example.com" in emails
    assert "support@example.com" in emails
    assert "noreply@example.com" not in emails