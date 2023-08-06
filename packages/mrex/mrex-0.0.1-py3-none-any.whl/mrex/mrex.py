from __future__ import annotations

import re
from typing import Iterator, Optional


class MagicRegex:
    def __init__(self, text: str):
        self._text = text
        self._compiled_re = None

    @property
    def text(self):
        if self._text is None:
            self._text = ''
        return self._text

    @property
    def regex(self):
        if self._compiled_re is None:
            self._compiled_re = re.compile(self.text)
        return self._compiled_re

    def find(self, text: str) -> Optional[re.Match[str]]:
        return self.regex.search(text)

    def find_all(self, text: str) -> Iterator[re.Match[str]]:
        return self.regex.finditer(text)

    def repeat(self, n: int) -> MagicRegex:
        return MagicRegex(f'(?:{self._text}){{{n}}}')

    def repeat_min_max(self, n: int, m: int) -> MagicRegex:
        return MagicRegex(f'(?:{self._text}){{{n},{m}}}')

    def repeat_zero_or_more(self) -> MagicRegex:
        return MagicRegex(f'(?:{self._text})*')

    def repeat_one_or_more(self) -> MagicRegex:
        return MagicRegex(f'(?:{self._text})+')

    def optional(self) -> MagicRegex:
        return MagicRegex(f'(?:{self._text})?')

    def group_as(self, name: str) -> MagicRegex:
        return MagicRegex(f'(?P<{name}>{self._text})')

    def or_(self, other: str | MagicRegex) -> MagicRegex:
        other_rex = other if isinstance(other, MagicRegex) else MagicRegex(other)
        return MagicRegex(f'(?:{self._text})|(?:{other_rex._text})')

    def and_(self, other: str | MagicRegex) -> MagicRegex:
        other_rex = other if isinstance(other, MagicRegex) else MagicRegex(other)
        return MagicRegex(f'(?:{self._text})(?:{other_rex._text})')


def exactly(text: str) -> MagicRegex:
    escaped_text = re.escape(text)
    return MagicRegex(escaped_text)

def char_in(chars: str) -> MagicRegex:
    escaped_chars = re.escape(chars)
    return MagicRegex(f'[{escaped_chars}]')

def char_not_in(chars: str) -> MagicRegex:
    escaped_chars = re.escape(chars)
    return MagicRegex(f'[^{escaped_chars}]')
