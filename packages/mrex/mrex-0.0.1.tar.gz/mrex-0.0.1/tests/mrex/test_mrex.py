import mrex


def test_exactly_should_return_object_on_match_success():
    text = '!@#$%^&*()'
    assert mrex.exactly(text).find(text) is not None

def test_exactly_should_return_none_on_match_fail():
    text = '!@#$%^&*()'
    assert mrex.exactly(text).find(text[:-1]) is None

def test_chars_in_should_return_object_on_match_success():
    chars = 'a][b'
    assert mrex.char_in(chars).find(chars[-1]) is not None

def test_chars_in_should_return_None_on_match_fail():
    chars = 'a][b'
    assert mrex.char_in(chars).find('c') is None

def test_chars_not_in_should_return_object_on_match_success():
    chars = 'a][b'
    assert mrex.char_not_in(chars).find('c') is not None

def test_chars_not_in_should_return_none_on_match_fail():
    chars = 'a][b'
    assert mrex.char_not_in(chars).find(chars[-1]) is None
