from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from better_translation._babel.extractor import extract_from_dir
from better_translation.types import (
    ITranslation,
    Locale,
    Message,
    RawSingular,
)

if TYPE_CHECKING:
    from collections.abc import Iterable
    from os import PathLike

logger = logging.getLogger(__name__)


class IStorage(ABC):
    @abstractmethod
    def get_translation(
        self,
        raw_singular: RawSingular,
        locale: Locale,
    ) -> ITranslation | None:
        """Get a translation for a message."""

    @abstractmethod
    async def load(self) -> None:
        """Load translations from the storage to the memory."""

    @abstractmethod
    async def update_messages(
        self,
        directory_path: str | PathLike[str],
    ) -> None:
        """Update untranslated messages from the directory in the storage."""


@dataclass(slots=True)
class BaseStorage(IStorage, ABC):
    storage: dict[str | RawSingular, dict[str | Locale, ITranslation]] = field(
        default_factory=dict,
        init=False,
    )
    is_loaded: bool = field(default=False, init=False)

    def get_translation(
        self,
        raw_singular: RawSingular,
        locale: Locale,
    ) -> ITranslation | None:
        """Get a translation for a message."""
        if not self.is_loaded:
            msg = "Cannot get translation, storage is not loaded..."
            raise ValueError(msg)

        return self.storage.get(raw_singular, {}).get(locale)

    def _extract_messages(
        self,
        directory_path: str | PathLike[str],
    ) -> Iterable[Message]:
        """Extract messages from the source."""
        extracted_messages = extract_from_dir(directory_path)

        for extracted_message in extracted_messages:
            logger.debug("Extracted message: %s", extracted_message)
            (
                filename,
                lineno,
                messages,
                _comments,
                _context,
            ) = extracted_message

            if isinstance(messages, str):
                raw_singular, raw_plural = messages, ""
            else:
                raw_singular, raw_plural = messages

            message = Message(
                raw_singular=raw_singular,  # type: ignore[arg-type]
                raw_plural=raw_plural,  # type: ignore[arg-type]
                filename=filename,
                lineno=lineno,
            )
            logger.debug("Extracted message: %s", message)
            yield message
