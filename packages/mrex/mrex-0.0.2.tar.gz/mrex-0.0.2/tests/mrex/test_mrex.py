import mrex


def test_exactly_should_return_object_on_match_success():
    text = "!@#$%^&*()"
    assert mrex.exactly(text).find(text) is not None


def test_exactly_should_return_none_on_match_fail():
    text = "!@#$%^&*()"
    assert mrex.exactly(text).find(text[:-1]) is None


def test_chars_in_should_return_object_on_match_success():
    chars = "a][b"
    assert mrex.char_in(chars).find(chars[-1]) is not None


def test_chars_in_should_return_None_on_match_fail():
    chars = "a][b"
    assert mrex.char_in(chars).find("c") is None


def test_chars_not_in_should_return_object_on_match_success():
    chars = "a][b"
    assert mrex.char_not_in(chars).find("c") is not None


def test_chars_not_in_should_return_none_on_match_fail():
    chars = "a][b"
    assert mrex.char_not_in(chars).find(chars[-1]) is None


def test_any_of_should_return_object_on_match_success():
    words = ["hello", "world", "!!!"]
    mrex_obj = mrex.any_of(words)
    assert mrex_obj.find(words[0]) is not None
    assert mrex_obj.find(words[1]) is not None
    assert mrex_obj.find(words[2]) is not None


def test_any_of_should_return_none_on_match_failure():
    words = ["hello", "world", "!!!"]
    mrex_obj = mrex.any_of(words)
    assert mrex_obj.find("hola") is None
