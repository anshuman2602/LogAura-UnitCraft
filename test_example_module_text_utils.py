import pytest

from example_module_text_utils import (
    normalize_whitespace,
    is_palindrome,
    word_count,
    unique_words,
    truncate,
    batch_normalize,
)


@pytest.mark.positive
@pytest.mark.parametrize(
    "text,expected",
    [
        ("  hello   world \n", "hello world"),
        ("\t a \n b  \t", "a b"),
        ("", ""),
        ("already ok", "already ok"),
        ("   \t\n  ", ""),
    ],
)
def test_normalize_whitespace_happy(text, expected):
    assert normalize_whitespace(text) == expected


@pytest.mark.negative
@pytest.mark.parametrize("bad", [None, 123, [], object()])
def test_normalize_whitespace_type_error(bad):
    with pytest.raises(TypeError, match="text must be a string"):
        normalize_whitespace(bad)  # type: ignore[arg-type]


@pytest.mark.positive
@pytest.mark.parametrize(
    "text",
    [
        "A man, a plan, a canal: Panama",
        "No 'x' in Nixon",
        "1221",
        "",
        ".,! ",  # only non-alphanumeric -> empty string -> palindrome
    ],
)
def test_is_palindrome_true_default(text):
    assert is_palindrome(text) is True


@pytest.mark.positive
@pytest.mark.parametrize(
    "text",
    [
        "hello",
        "abca",
        "1231",
        "ab",
    ],
)
def test_is_palindrome_false_default(text):
    assert is_palindrome(text) is False


@pytest.mark.positive
@pytest.mark.parametrize(
    "text",
    [
        "RacecaR",
        "abba",
    ],
)
def test_is_palindrome_true_ignore_case_false(text):
    assert is_palindrome(text, ignore_case=False) is True


@pytest.mark.positive
@pytest.mark.parametrize(
    "text",
    [
        "Abba",  # case mismatch makes it not a palindrome when case-sensitive
        "hello",
    ],
)
def test_is_palindrome_false_ignore_case_false(text):
    assert is_palindrome(text, ignore_case=False) is False


@pytest.mark.negative
@pytest.mark.parametrize("bad", [None, 3.14, 0, [], {}])
def test_is_palindrome_type_error(bad):
    with pytest.raises(TypeError, match="text must be a string"):
        is_palindrome(bad)  # type: ignore[arg-type]


@pytest.mark.positive
@pytest.mark.parametrize(
    "text,expected",
    [
        ("hello world", 2),
        ("  hello   world \n", 2),
        ("", 0),
        ("   ", 0),
        ("single", 1),
        ("a\tb\nc", 3),
    ],
)
def test_word_count_happy(text, expected):
    assert word_count(text) == expected


@pytest.mark.negative
@pytest.mark.parametrize("bad", [None, 1, 1.0, ["a", "b"], {}])
def test_word_count_type_error(bad):
    with pytest.raises(TypeError, match="text must be a string"):
        word_count(bad)  # type: ignore[arg-type]


@pytest.mark.positive
def test_unique_words_defaults_happy():
    text = "Hello, hello world! world2 123"
    assert unique_words(text) == ["123", "hello", "world", "world2"]


@pytest.mark.positive
def test_unique_words_ignore_case_false_happy():
    text = "Hello hello HELLO"
    assert unique_words(text, ignore_case=False) == ["HELLO", "Hello", "hello"]


@pytest.mark.positive
@pytest.mark.parametrize(
    "text,min_length,expected",
    [
        ("a an and android", 1, ["a", "an", "and", "android"]),
        ("a an and android", 2, ["an", "and", "android"]),
        ("a an and android", 3, ["and", "android"]),
        ("1 22 333", 2, ["22", "333"]),
    ],
)
def test_unique_words_min_length_happy(text, min_length, expected):
    assert unique_words(text, min_length=min_length) == expected


@pytest.mark.positive
def test_unique_words_empty_text_happy():
    assert unique_words("") == []


@pytest.mark.negative
@pytest.mark.parametrize("bad", [None, 5, 3.14, [], {}])
def test_unique_words_type_error(bad):
    with pytest.raises(TypeError, match="text must be a string"):
        unique_words(bad)  # type: ignore[arg-type]


@pytest.mark.negative
@pytest.mark.parametrize("min_length", [0, -1, -10])
def test_unique_words_min_length_value_error(min_length):
    with pytest.raises(ValueError, match=">= 1"):
        unique_words("anything", min_length=min_length)


@pytest.mark.positive
@pytest.mark.parametrize(
    "text,max_length,expected",
    [
        ("hello", 5, "hello"),  # equal length
        ("hello", 10, "hello"),  # less than max
        ("", 0, ""),  # empty text
    ],
)
def test_truncate_no_truncation_happy(text, max_length, expected):
    assert truncate(text, max_length) == expected


@pytest.mark.positive
@pytest.mark.parametrize(
    "text,max_length,expected",
    [
        ("hello world", 5, "he..."),
        ("abcdef", 3, "..."),  # exact suffix length
    ],
)
def test_truncate_with_default_suffix_happy(text, max_length, expected):
    assert truncate(text, max_length) == expected


@pytest.mark.positive
def test_truncate_with_custom_suffix_happy():
    assert truncate("abcdef", 4, suffix="--") == "ab--"


@pytest.mark.positive
@pytest.mark.parametrize(
    "text,max_length,expected",
    [
        ("abcdef", 2, ".."),
        ("abcdef", 0, ""),
    ],
)
def test_truncate_when_max_less_than_suffix_happy(text, max_length, expected):
    assert truncate(text, max_length) == expected


@pytest.mark.negative
def test_truncate_type_error_text():
    with pytest.raises(TypeError, match="text must be a string"):
        truncate(None, 5)  # type: ignore[arg-type]


@pytest.mark.negative
def test_truncate_value_error_negative_max_length():
    with pytest.raises(ValueError, match=">= 0"):
        truncate("abc", -1)


@pytest.mark.negative
def test_truncate_type_error_non_string_suffix():
    # suffix must be sliceable like a string; non-string raises TypeError
    with pytest.raises(TypeError):
        truncate("abcdef", 2, suffix=5)  # type: ignore[arg-type]


@pytest.mark.positive
@pytest.mark.parametrize(
    "texts,expected",
    [
        (["  a  b ", " c   d"], ["a b", "c d"]),
        ((t for t in [" x ", " y\t z "]), ["x", "y z"]),
        ([], []),
        ((t for t in []), []),
    ],
)
def test_batch_normalize_happy(texts, expected):
    assert batch_normalize(texts) == expected


@pytest.mark.negative
def test_batch_normalize_none_raises():
    with pytest.raises(TypeError, match="texts cannot be None"):
        batch_normalize(None)  # type: ignore[arg-type]


@pytest.mark.negative
def test_batch_normalize_element_type_error():
    with pytest.raises(TypeError, match="text must be a string"):
        batch_normalize(["ok", 1])  # inner normalize_whitespace raises