import pytest
from example_module_text_utils import (
    normalize_whitespace,
    is_palindrome,
    word_count,
)


@pytest.mark.positive
@pytest.mark.parametrize(
    "text,expected",
    [
        ("  hello   world \n", "hello world"),
        ("a\tb\nc", "a b c"),
        ("single", "single"),
        ("  leading   and   trailing  ", "leading and trailing"),
    ],
)
def test_normalize_whitespace_basic_cases(text, expected):
    assert normalize_whitespace(text) == expected


@pytest.mark.negative
def test_normalize_whitespace_empty_string_edge():
    assert normalize_whitespace("") == ""


@pytest.mark.negative
@pytest.mark.parametrize("bad", [None, 123, 12.3, [], {}, object()])
def test_normalize_whitespace_type_error(bad):
    with pytest.raises(TypeError):
        normalize_whitespace(bad)  # type: ignore[arg-type]


@pytest.mark.positive
@pytest.mark.parametrize(
    "text,kwargs,expected",
    [
        ("A man, a plan, a canal: Panama", {}, True),
        ("racecar", {}, True),
        ("aa", {"ignore_case": False}, True),
    ],
)
def test_is_palindrome_true_cases(text, kwargs, expected):
    assert is_palindrome(text, **kwargs) == expected


@pytest.mark.negative
@pytest.mark.parametrize(
    "text,kwargs,expected",
    [
        ("hello", {}, False),
        ("Aa", {"ignore_case": False}, False),
    ],
)
def test_is_palindrome_non_palindromes(text, kwargs, expected):
    assert is_palindrome(text, **kwargs) == expected


@pytest.mark.negative
@pytest.mark.parametrize("text", ["", "!!!", " , . "])
def test_is_palindrome_edge_cases_true(text):
    # Edge cases: empty or only non-alphanumeric characters are considered palindromes
    assert is_palindrome(text) is True


@pytest.mark.negative
@pytest.mark.parametrize("bad", [None, 123, 12.3, [], {}, object()])
def test_is_palindrome_type_error(bad):
    with pytest.raises(TypeError):
        is_palindrome(bad)  # type: ignore[arg-type]


@pytest.mark.positive
@pytest.mark.parametrize(
    "text,expected",
    [
        ("hello world", 2),
        ("hello, world!", 2),
        ("a  b\n c\t d", 4),
        ("  hi ", 1),
    ],
)
def test_word_count_basic(text, expected):
    assert word_count(text) == expected


@pytest.mark.negative
@pytest.mark.parametrize("text", ["", "   \n\t  "])
def test_word_count_zero_cases(text):
    assert word_count(text) == 0


@pytest.mark.negative
@pytest.mark.parametrize("bad", [None, 123, 12.3, [], {}, object()])
def test_word_count_type_error(bad):
    with pytest.raises(TypeError):
        word_count(bad)  # type: ignore[arg-type]