# Copyright (C) 2016-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import collections
from typing import Any

from .messagehandler import MessageHandler
from .sewer import Sewer
from .types import Envelope


class Provider:
    __module__: str = 'aorta'
    __handlers__: dict[tuple[str, str], set[type[MessageHandler]]] = collections.defaultdict(set)
    __sewers__: set[type[Sewer]] = set()

    @classmethod
    def register(cls, handler_class: type[MessageHandler]) -> None:
        """Register a message handler implementation."""
        if issubclass(handler_class, Sewer):
            cls.__sewers__.add(handler_class)
            return

        for Message in handler_class.handles:
            k = (getattr(Message, '__version__', 'v1'), Message.__name__)
            cls.__handlers__[k].add(handler_class)

    @classmethod
    def get(cls, envelope: Envelope[Any], sewers: bool = True) -> set[type[MessageHandler]]:
        """Get the set of message handlers that are able to handle the
        message contained in the envelope.
        """
        handlers = set(cls.__handlers__[envelope.qualname])
        if sewers:
            handlers |= set(cls.__sewers__)
        return handlers
    
    @classmethod
    def num_sewers(cls) -> int:
        return len(cls.__sewers__)