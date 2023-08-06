import mrex

# exactly()


def test_exactly_should_return_object_on_match_success():
    text = "!@#$%^&*()"
    assert mrex.exactly(text).find(text) is not None


def test_exactly_should_return_none_on_match_fail():
    text = "!@#$%^&*()"
    assert mrex.exactly(text).find(text[:-1]) is None


# chars_in()


def test_chars_in_should_return_object_on_match_success():
    chars = "a][b"
    assert mrex.char_in(chars).find(chars[-1]) is not None


def test_chars_in_should_return_None_on_match_fail():
    chars = "a][b"
    assert mrex.char_in(chars).find("c") is None


# chars_not_in()


def test_chars_not_in_should_return_object_on_match_success():
    chars = "a][b"
    assert mrex.char_not_in(chars).find("c") is not None


def test_chars_not_in_should_return_none_on_match_fail():
    chars = "a][b"
    assert mrex.char_not_in(chars).find(chars[-1]) is None


# any_of()


def test_any_of_should_return_object_on_match_success():
    words = ["hello", "world", "!!!"]
    mrex_obj = mrex.any_of(words)
    assert mrex_obj.find(words[0]) is not None
    assert mrex_obj.find(words[1]) is not None
    assert mrex_obj.find(words[2]) is not None


def test_any_of_should_return_none_on_match_fail():
    words = ["hello", "world", "!!!"]
    mrex_obj = mrex.any_of(words)
    assert mrex_obj.find("hola") is None


# concat()


def test_concat_should_return_object_on_match_success():
    words = ["hello", "world", "!!!"]
    assert mrex.concat(words).find("".join(words)) is not None


def test_concat_should_return_none_on_match_fail():
    words = ["hello", "world", "!!!"]
    assert mrex.concat(words).find(" ".join(words)) is None


# repeat()


def test_repeat_should_match_on_success():
    assert mrex.DIGIT.repeat(3).find("aA12345").group() == "123"


def test_repeat_should_return_none_on_fail():
    assert mrex.DIGIT.repeat(3).find("aA12") is None


# repeat_zero_or_more()


def test_repeat_zero_or_more_should_match_on_success():
    text = "!@#$%^&*()_+"
    mrex_obj = mrex.exactly(text).repeat_zero_or_more()
    assert mrex_obj.find(text).group() == text
    assert mrex_obj.find(text * 2).group() == text * 2
    assert mrex_obj.find("!!!").group() == ""


# repeat_one_or_more()


def test_repeat_one_or_more_should_match_on_success():
    text = "!@#$%^&*()_+"
    mrex_obj = mrex.exactly(text).repeat_zero_or_more()
    assert mrex_obj.find(text).group() == text
    assert mrex_obj.find(text * 2).group() == text * 2


def test_repeat_one_or_more_should_return_none_on_fail():
    assert mrex.DIGIT.repeat_one_or_more().find("abcde") is None


# optional()


def test_optional_should_return_match_on_success():
    text = "!@#$%^&*()_+"
    mrex_obj = mrex.exactly(text).optional()
    assert mrex_obj.find(text).group() == text
    assert mrex_obj.find(text * 2).group() == text
    assert mrex_obj.find("").group() == ""


# find_all()


def test_find_all_should_return_multiple_matches():
    assert mrex.DIGITS.find_all("1 23 456") == ["1", "23", "456"]


# group_as()


def test_group_as_should_return_grouped_match():
    name = "group_name"
    text = "!@#$%^&*()_+"
    assert mrex.ALL.group_as(name).find(text).group(name) == text


# or_()


def test_or_should_return_match_on_either_input():
    mrex_obj = mrex.DIGITS.or_(mrex.CHARS)
    assert mrex_obj.find("123").group() == "123"
    assert mrex_obj.find("abc").group() == "abc"


def test_or_should_return_none_on_match_fail():
    assert mrex.DIGITS.or_(mrex.CHARS).find("!!!") is None


# and_()


def test_and_should_return_match_on_success():
    assert mrex.DIGITS.and_(mrex.NON_DIGITS).find("123abc").group() == "123abc"


def test_and_should_return_none_on_match_fail():
    assert mrex.DIGITS.and_(mrex.NON_DIGITS).find("abc123") is None
