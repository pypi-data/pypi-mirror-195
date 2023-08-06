from typing import Sequence, Union

from tbot_api import enums, types

from ....filters import Filter


class ContentTypes(Filter):
    def __init__(
        self, content_type: Union[enums.ContentType, Sequence[enums.ContentType]]
    ) -> None:
        self.content_type = (
            {content_type} if isinstance(content_type, enums.ChatType) else set(content_type)
        )

    async def __call__(self, update: types.Message) -> bool:
        if not isinstance(update, types.Message):
            return False
        return update.content_type in self.content_type
