from __future__ import annotations

import re
from typing import Iterator, Optional


class MagicRegex:
    def __init__(self, text: str):
        self._text = text
        self._regex = None

    @property
    def text(self):
        return self._text

    @property
    def regex(self):
        if self._regex is None:
            self._regex = re.compile(self.text)
        return self._regex

    # Match

    def find(self, text: str) -> Optional[re.Match[str]]:
        return self.regex.search(text)

    def find_all(self, text: str) -> Iterator[re.Match[str]]:
        return self.regex.finditer(text)

    # Repeat

    def repeat(self, n: int) -> MagicRegex:
        return MagicRegex(f"(?:{self._text}){{{n}}}")

    def repeat_min_max(self, n: int, m: int) -> MagicRegex:
        return MagicRegex(f"(?:{self._text}){{{n},{m}}}")

    def repeat_zero_or_more(self) -> MagicRegex:
        return MagicRegex(f"(?:{self._text})*")

    def repeat_one_or_more(self) -> MagicRegex:
        return MagicRegex(f"(?:{self._text})+")

    def optional(self) -> MagicRegex:
        return MagicRegex(f"(?:{self._text})?")

    # Group

    def group_as(self, name: str) -> MagicRegex:
        return MagicRegex(f"(?P<{name}>{self._text})")

    # Concat

    def or_(self, other: str | MagicRegex) -> MagicRegex:
        other_rex = other if isinstance(other, MagicRegex) else MagicRegex(other)
        return MagicRegex(f"(?:{self._text})|(?:{other_rex._text})")

    def and_(self, other: str | MagicRegex) -> MagicRegex:
        other_rex = other if isinstance(other, MagicRegex) else MagicRegex(other)
        return MagicRegex(f"(?:{self._text})(?:{other_rex._text})")


def exactly(text: str) -> MagicRegex:
    escaped_text = re.escape(text)
    return MagicRegex(escaped_text)


def char_in(chars: str) -> MagicRegex:
    escaped_chars = re.escape(chars)
    return MagicRegex(f"[{escaped_chars}]")


def char_not_in(chars: str) -> MagicRegex:
    escaped_chars = re.escape(chars)
    return MagicRegex(f"[^{escaped_chars}]")


def any_of(options: list[str | MagicRegex]) -> MagicRegex:
    options_objects = [
        option if isinstance(option, MagicRegex) else exactly(option)
        for option in options
    ]
    any_of_str = "|".join([f"(?:{match.text})" for match in options_objects])
    return MagicRegex(any_of_str)
