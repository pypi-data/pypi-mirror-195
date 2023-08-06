import mrex


def test_digit_should_return_first_digit_on_success():
    assert mrex.DIGIT.find("123").group() == "1"


def test_digit_should_return_none_on_failue():
    assert mrex.DIGIT.find("abc") is None


def test_digits_should_return_all_digits_on_success():
    assert mrex.DIGITS.find("123").group() == "123"


def test_digits_should_return_none_on_failue():
    assert mrex.DIGITS.find("abc") is None


def test_char_should_return_first_char_on_success():
    assert mrex.CHAR.find("aA_123").group() == "a"


def test_char_should_return_none_on_failue():
    assert mrex.CHAR.find("!@#") is None


def test_chars_should_return_all_chars_on_success():
    assert mrex.CHARS.find("aA_123").group() == "aA_123"


def test_chars_should_return_none_on_failue():
    assert mrex.CHARS.find("!@#") is None
