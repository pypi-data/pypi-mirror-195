from __future__ import annotations

from dataclasses import dataclass
from typing import Any, NewType, Protocol

Locale = NewType("Locale", str)

RawText = NewType("RawText", str)
RawSingular = NewType("RawSingular", RawText)
RawPlural = NewType("RawPlural", RawText)

TranslatedText = NewType("TranslatedText", str)
TranslatedSingular = NewType("TranslatedSingular", TranslatedText)
TranslatedPlural = NewType("TranslatedPlural", TranslatedText)


@dataclass(slots=True, frozen=True)
class Message:
    raw_singular: RawSingular
    raw_plural: RawPlural | None
    filename: str
    lineno: int


class ITranslation(Protocol):
    locale: Locale | Any
    singular: str | TranslatedSingular | Any
    plural: str | TranslatedPlural | Any
