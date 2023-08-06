import string

from .mrex import MagicRegex, char_in

# A single digit
DIGIT = MagicRegex(r"\d")
# One or mor digits
DIGITS = DIGIT.repeat_one_or_more()

# Any non-digit character
NON_DIGIT = MagicRegex(r"\D")
# One or more non-digit characters
NON_DIGITS = NON_DIGIT.repeat_one_or_more()

# A single character in [a-zA-Z0-9_] (uppercase, lowercase, digit, or '_')
CHAR = MagicRegex(r"\w")
# One or more characters in [a-zA-Z0-9_] (uppercase, lowercase, digit, or '_')
CHARS = CHAR.repeat_one_or_more()

# A single character not in [a-zA-Z0-9_] (uppercase, lowercase, digit, or '_')
NON_CHAR = MagicRegex(r"\W")
# One or more characters not in [a-zA-Z0-9_] (uppercase, lowercase, digit, or '_')
NON_CHARS = NON_CHAR.repeat_one_or_more()

# A single whitespace character
SPACE = MagicRegex(r"\s")
# One or more whitespace characters
SPACES = SPACE.repeat_one_or_more()

# A single non-whitespace character
NON_SPACE = MagicRegex(r"\S")
# One or more non-whitespace characters
NON_SPACES = NON_SPACE.repeat_one_or_more()

# A single lowercase character
LOWERCASE = char_in(string.ascii_lowercase)
# A single uppercase character
UPPERCASE = char_in(string.ascii_uppercase)
