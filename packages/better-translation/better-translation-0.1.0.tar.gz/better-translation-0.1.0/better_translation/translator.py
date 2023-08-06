from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from better_translation.storage import IStorage
    from better_translation.types import (
        Locale,
        RawPlural,
        RawSingular,
        TranslatedPlural,
        TranslatedSingular,
        TranslatedText,
    )


logger = logging.getLogger(__name__)


class ITranslator(ABC):
    @abstractmethod
    def translate(
        self,
        locale: Locale,
        raw_singular: RawSingular,
        raw_plural: RawPlural | None = None,
        n: int = 1,
    ) -> TranslatedText:
        ...


@dataclass(slots=True)
class DefaultTranslator(ITranslator):
    storage: IStorage

    def translate(
        self,
        locale: Locale,
        raw_singular: RawSingular,
        raw_plural: RawPlural | None = None,
        n: int = 1,
    ) -> TranslatedText:
        if raw_plural is None:
            return self._translate_singular(locale, raw_singular)

        return self._translate_plural(
            locale,
            raw_singular,
            raw_plural,
            n,
        )

    def _translate_singular(
        self,
        locale: Locale,
        raw_singular: RawSingular,
    ) -> TranslatedSingular:
        translation = self.storage.get_translation(raw_singular, locale)
        logger.debug(
            "Translating for '%s' in '%s' -> '%s'",
            raw_singular,
            locale,
            translation,
        )
        return (
            translation.singular  # type: ignore[return-value]
            if translation is not None
            else raw_singular
        )

    def _translate_plural(
        self,
        locale: Locale,
        raw_singular: RawSingular,
        raw_plural: RawPlural,
        n: int,
    ) -> TranslatedPlural:
        translation = self.storage.get_translation(raw_singular, locale)

        logger.debug(
            "Translating for '%s' in '%s' -> '%s'",
            raw_singular,
            locale,
            translation,
        )

        singular: RawSingular | str | TranslatedSingular | Any
        plural: RawPlural | str | TranslatedPlural | Any

        if translation is None:
            singular, plural = raw_singular, raw_plural
        else:
            singular, plural = translation.singular, translation.plural

        return singular if n == 1 else plural  # type: ignore[return-value]
