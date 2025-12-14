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

