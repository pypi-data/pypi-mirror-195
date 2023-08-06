from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING

from better_translation.integrations.django.models import BaseMessage
from better_translation.storage import BaseStorage

if TYPE_CHECKING:
    from os import PathLike

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class DjangoStorage(BaseStorage):
    message_model: type[BaseMessage] = BaseMessage

    def __post_init__(self) -> None:
        if self.message_model is BaseMessage:
            msg = "`message_model` is required"
            raise ValueError(msg)

    async def load(self) -> None:
        """Load translations from the storage to the memory."""
        logger.info("Loading messages from the database...")

        messages = self.message_model.objects.all().prefetch_related(
            "translations",
        )
        async for message in messages:
            translations = message.translations.all()
            if not translations:
                logger.warning(
                    "Message '%s' has no translations",
                    message,
                )
            else:
                logger.debug(
                    "Message '%s' has '%s' translations",
                    message,
                    len(translations),
                )

            self.storage[message.raw_singular] = {
                translation.locale: translation for translation in translations
            }

        self.is_loaded = True

        logger.info("Messages loaded successfully")

    async def update_messages(
        self,
        directory_path: str | PathLike[str],
    ) -> None:
        if not self.is_loaded:
            logger.info("Cannot update messages, storage is not loaded...")
            await self.load()

        logger.info("Updating messages from the directory...")

        new_messages: set[BaseMessage] = set()
        unused_messages = set(self.storage)

        messages = self._extract_messages(directory_path)
        for message in messages:
            if message.raw_singular in self.storage:
                unused_messages.remove(message.raw_singular)
                continue

            logger.debug(
                "Message '%s' is new, adding to the database...",
                message,
            )
            new_messages.add(
                self.message_model(
                    raw_singular=message.raw_singular,
                    raw_plural=message.raw_plural,
                    filename=message.filename,
                    lineno=message.lineno,
                ),
            )
            self.storage[message.raw_singular] = {}

        tasks = (
            self.message_model.objects.abulk_create(new_messages),
            self.message_model.objects.filter(
                raw_singular__in=self.storage,
            )
            .exclude(
                raw_singular__in=unused_messages,
            )
            .aupdate(is_used=True),
            self.message_model.objects.filter(
                raw_singular__in=unused_messages,
            )
            .exclude(
                raw_singular__in=self.storage,
            )
            .aupdate(is_used=False),
        )

        _ = await asyncio.gather(*tasks)

        logger.info("Messages updated successfully")
