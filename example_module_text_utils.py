"""
text_utils.py

Small utility functions for working with text.
Designed to be easy to unit test.
"""

import re
from typing import Iterable, List


def normalize_whitespace(text: str) -> str:
    """
    Replace multiple whitespace characters with a single space
    and strip leading/trailing whitespace.

    Example:
        "  hello   world \n" -> "hello world"
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    return re.sub(r"\s+", " ", text).strip()


def is_palindrome(text: str, *, ignore_case: bool = True) -> bool:
    """
    Check whether a string is a palindrome.
    Non-alphanumeric characters are ignored.

    Example:
        "A man, a plan, a canal: Panama" -> True
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    filtered = "".join(ch for ch in text if ch.isalnum())

    if ignore_case:
        filtered = filtered.lower()

    return filtered == filtered[::-1]


def word_count(text: str) -> int:
    """
    Count number of words in a string.
    Words are separated by whitespace.

    Example:
        "hello world" -> 2
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    text = normalize_whitespace(text)
    if not text:
        return 0

    return len(text.split(" "))


def unique_words(
    text: str,
    *,
    ignore_case: bool = True,
    min_length: int = 1
) -> List[str]:
    """
    Return a sorted list of unique words from the text.

    Parameters:
        ignore_case: treat 'Hello' and 'hello' as the same word
        min_length: minimum word length to include

    Example:
        "Hello hello world!" -> ["hello", "world"]
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    if min_length < 1:
        raise ValueError("min_length must be >= 1")

    words = re.findall(r"\b\w+\b", text)

    if ignore_case:
        words = [w.lower() for w in words]

    return sorted({w for w in words if len(w) >= min_length})


def truncate(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Truncate text to max_length characters.
    Appends suffix if truncation occurs.

    Example:
        truncate("hello world", 5) -> "he..."
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    if max_length < 0:
        raise ValueError("max_length must be >= 0")

    if len(text) <= max_length:
        return text

    if max_length < len(suffix):
        return suffix[:max_length]

    return text[: max_length - len(suffix)] + suffix


def batch_normalize(texts: Iterable[str]) -> List[str]:
    """
    Normalize whitespace for multiple strings.

    Example:
        ["  a  b ", " c   d"] -> ["a b", "c d"]
    """
    if texts is None:
        raise TypeError("texts cannot be None")

    return [normalize_whitespace(t) for t in texts]
