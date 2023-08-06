from .mrex import MagicRegex


def digit():
    return MagicRegex('\d')

def non_digit():
    return MagicRegex('\D')

def character():
    return MagicRegex('\w')

def non_character():
    return MagicRegex('\W')

def whitespace():
    return MagicRegex('\s')

def non_space():
    return MagicRegex('\S')

def ipv4():
    ipv4_number = MagicRegex(r'25[0-5]').or_(r'2[0-4]\d').or_(r'1\d\d').or_(r'[1-9]\d').or_(r'\d')
    number_dot = ipv4_number.and_(r'\.')
    return number_dot.repeat(3).and_(ipv4_number)

def email():
    user = MagicRegex(r'[\w-\.]').repeat_one_or_more()
    domain = MagicRegex(r'[\w-]').repeat_one_or_more().and_(r'\.').repeat_one_or_more().and_(r'\w{2,4}')
    return user.and_('@').and_(domain)
