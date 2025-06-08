import pytest
from complex_math import _tokenize

def test_tokenize_numbers():
    assert _tokenize("123") == ["123"]
    assert _tokenize("12.34") == ["12.34"]

def test_tokenize_operators():
    assert _tokenize("1+2") == ["1", "+", "2"]
    assert _tokenize("3-4") == ["3", "-", "4"]
    assert _tokenize("5*6") == ["5", "*", "6"]
    assert _tokenize("7/8") == ["7", "/", "8"]

def test_tokenize_parentheses():
    assert _tokenize("(1+2)") == ["(", "1", "+", "2", ")"]

def test_tokenize_whitespace():
    assert _tokenize("1 + 2") == ["1", "+", "2"]

def test_tokenize_invalid_char():
    with pytest.raises(SyntaxError):
        _tokenize("1@2")

def test_tokenize_empty_num():
    assert _tokenize("+") == ["+"]
