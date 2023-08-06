# Copyright (C) 2016-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import logging
from typing import Any

from .types import Command
from .types import Envelope
from .types import Event
from .types import ITransaction
from .types import MessageMetadata


class MessageHandler:
    """The base class for all message handlers."""
    __module__: str = 'aorta'
    __abstract__: bool = True
    handles: list[type[Command] | type[Event]]
    logger: logging.Logger = logging.getLogger('aorta')
    metadata: MessageMetadata
    publisher: ITransaction

    def __init__(
        self,
        publisher: ITransaction,
        metadata: MessageMetadata
    ):
        self.metadata = MessageMetadata.parse_obj(metadata.dict())
        self.publisher = publisher
        assert metadata.correlation_id == self.metadata.correlation_id
        assert metadata == self.metadata

    def issue(self, command: Command, audience: set[str] | None = None):
        """Issue a command using the default command issuer."""
        assert self.metadata.correlation_id is not None
        self.publisher.publish(
            command,
            correlation_id=self.metadata.correlation_id,
            audience=audience
        )

    async def on_exception(self, exception: Exception) -> None:
        """Hook to perform cleanup after a fatal exception.
        """
        pass

    def publish(self, event: Event, audience: set[str] | None = None):
        """Publish an event using the default event publisher."""
        assert self.metadata.correlation_id is not None
        self.publisher.publish(
            event,
            correlation_id=self.metadata.correlation_id,
            audience=audience
        )

    async def run(self, envelope: Envelope[Any]) -> tuple[bool, Any]:
        result: Any = NotImplemented
        success = False
        try:
            result = await self.handle(envelope.message.parse_obj(envelope.message)) # type: ignore
            success = True
        except Exception as e: # pragma: no cover
            await self.on_exception(e)
            raise
        return success, result
