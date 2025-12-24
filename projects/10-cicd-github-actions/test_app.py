import pytest
from app import transform_currency, clean_name

def test_transform_currency_happy_path():
    assert transform_currency(100, 1.2) == 120.00

def test_transform_currency_negative():
    with pytest.raises(ValueError):
        transform_currency(-50, 1.2)

def test_clean_name_dirty():
    assert clean_name("  alice  ") == "Alice"

def test_clean_name_none():
    assert clean_name(None) == "Unknown"
