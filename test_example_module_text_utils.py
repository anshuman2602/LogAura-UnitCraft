import pytest
import example_module_text_utils as tu


# normalize_whitespace
@pytest.mark.positive
def test_normalize_whitespace_mixed():
    assert tu.normalize_whitespace("\t Hello\n\n   world\t\t") == "Hello world"


@pytest.mark.negative
def test_normalize_whitespace_non_string_raises():
    with pytest.raises(TypeError):
        tu.normalize_whitespace(123)  # type: ignore[arg-type]


@pytest.mark.negative
def test_normalize_whitespace_only_spaces_to_empty():
    assert tu.normalize_whitespace("   \n\t   ") == ""


# is_palindrome
@pytest.mark.positive
def test_is_palindrome_phrase_ignore_case_true():
    assert tu.is_palindrome("A man, a plan, a canal: Panama", ignore_case=True) is True


@pytest.mark.positive
def test_is_palindrome_numeric():
    assert tu.is_palindrome("12321") is True


@pytest.mark.positive
def test_is_palindrome_ignore_case_false_branch():
    # same letters different case should not be palindrome when ignore_case=False
    assert tu.is_palindrome("Aa", ignore_case=False) is False


@pytest.mark.negative
def test_is_palindrome_non_string_raises():
    with pytest.raises(TypeError):
        tu.is_palindrome(None)  # type: ignore[arg-type]


# word_count
@pytest.mark.positive
def test_word_count_irregular_spacing():
    assert tu.word_count("  hello\nworld\tthis   is   text  ") == 5


@pytest.mark.negative
def test_word_count_empty_or_whitespace_is_zero():
    assert tu.word_count("   \n\t  ") == 0


@pytest.mark.negative
def test_word_count_non_string_raises():
    with pytest.raises(TypeError):
        tu.word_count(3.14)  # type: ignore[arg-type]


# unique_words
@pytest.mark.positive
def test_unique_words_default_behavior():
    assert tu.unique_words("Hello, hello world!!!") == ["hello", "world"]


@pytest.mark.positive
def test_unique_words_case_sensitive_sorted_when_ignore_case_false():
    assert tu.unique_words("Hello hello world", ignore_case=False) == [
        "Hello",
        "hello",
        "world",
    ]


@pytest.mark.positive
def test_unique_words_min_length_filter():
    assert tu.unique_words("a bb ccc dddd", min_length=3) == ["ccc", "dddd"]


@pytest.mark.negative
def test_unique_words_min_length_lt_one_raises():
    with pytest.raises(ValueError):
        tu.unique_words("anything", min_length=0)


@pytest.mark.negative
def test_unique_words_non_string_raises():
    with pytest.raises(TypeError):
        tu.unique_words(42)  # type: ignore[arg-type]


# truncate
@pytest.mark.positive
def test_truncate_no_truncation_when_len_le_max():
    assert tu.truncate("hi", 5) == "hi"


@pytest.mark.positive
def test_truncate_with_default_suffix():
    assert tu.truncate("hello world", 5) == "he..."


@pytest.mark.positive
def test_truncate_max_length_less_than_suffix_length():
    assert tu.truncate("abcdef", 2) == ".."


@pytest.mark.positive
def test_truncate_with_custom_suffix():
    assert tu.truncate("abcdef", 5, suffix="!") == "abcd!"


@pytest.mark.negative
def test_truncate_non_string_raises():
    with pytest.raises(TypeError):
        tu.truncate(None, 3)  # type: ignore[arg-type]


@pytest.mark.negative
def test_truncate_negative_max_length_raises():
    with pytest.raises(ValueError):
        tu.truncate("abc", -1)


# batch_normalize
@pytest.mark.positive
def test_batch_normalize_with_list():
    assert tu.batch_normalize(["  a  b ", " c   d\t"]) == ["a b", "c d"]


@pytest.mark.positive
def test_batch_normalize_with_generator():
    gen = (s for s in ["  x\t y ", " z   w  "])
    assert tu.batch_normalize(gen) == ["x y", "z w"]


@pytest.mark.positive
def test_batch_normalize_empty_iterable():
    assert tu.batch_normalize([]) == []


@pytest.mark.negative
def test_batch_normalize_none_raises():
    with pytest.raises(TypeError):
        tu.batch_normalize(None)  # type: ignore[arg-type]


@pytest.mark.negative
def test_batch_normalize_propagates_typeerror_from_normalize():
    with pytest.raises(TypeError):
        tu.batch_normalize([1, " ok "])  # type: ignore[list-item]