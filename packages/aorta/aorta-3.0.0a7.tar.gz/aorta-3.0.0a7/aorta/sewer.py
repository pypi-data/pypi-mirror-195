# Copyright (C) 2016-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

from .types import Envelope
from .messagehandler import MessageHandler


class Sewer(MessageHandler):
    """A :class:`MessageHandler` implementation that is invoked for each
    incoming message, regardless of the type.
    """
    __module__: str = 'aorta'

    async def handle(self, message: Envelope[Any]) -> None:
        raise NotImplementedError