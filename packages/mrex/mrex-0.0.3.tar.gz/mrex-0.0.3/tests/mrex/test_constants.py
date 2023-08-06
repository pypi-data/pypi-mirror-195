import mrex

# DIGIT


def test_digit_should_return_first_digit_on_success():
    assert mrex.DIGIT.find("123").group() == "1"


def test_digit_should_return_none_on_failue():
    assert mrex.DIGIT.find("abc") is None


# DIGITS


def test_digits_should_return_all_digits_on_success():
    assert mrex.DIGITS.find("123").group() == "123"


def test_digits_should_return_none_on_failue():
    assert mrex.DIGITS.find("abc") is None


# CHAR


def test_char_should_return_first_char_on_success():
    assert mrex.CHAR.find("aA_123").group() == "a"


def test_char_should_return_none_on_failue():
    assert mrex.CHAR.find("!@#") is None


# CHARS


def test_chars_should_return_all_chars_on_success():
    assert mrex.CHARS.find("aA_123").group() == "aA_123"


def test_chars_should_return_none_on_failue():
    assert mrex.CHARS.find("!@#") is None


# ANY


def test_any_should_return_first_char_on_success():
    assert mrex.ANY.find("!@#").group() == "!"


def test_any_should_return_none_on_failure():
    assert mrex.ANY.find("") is None


# ALL


def test_all_should_return_all_chars_on_success():
    assert mrex.ALL.find("!@#\n").group() == "!@#\n"


def test_all_should_zero_match():
    assert mrex.ALL.find("") is not None
