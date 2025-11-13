thonfrom src.extractors.phone_extractor import extract_phone_numbers

def test_extract_phone_numbers_basic():
    text = """
    Call us at +1 (555) 123-4567 or 555-987-6543 today.
    """
    numbers = extract_phone_numbers(text)
    assert any("123-4567" in n for n in numbers)
    assert any("987-6543" in n for n in numbers)