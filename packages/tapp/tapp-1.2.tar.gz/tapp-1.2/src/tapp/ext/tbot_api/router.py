from __future__ import annotations

from typing import Any, Callable, Dict, Optional

from tbot_api.enums import UpdateType

from ...filters import Filter
from ...routing import TRouter as OriginalTRouter
from ...types import Decorated


class TRouter(OriginalTRouter):
    def message(
        self,
        *filters: Filter,
        flags: Optional[Dict[str, Any]] = None,
    ) -> Callable[[Decorated], Decorated]:
        return self.route(*filters, method=UpdateType.MESSAGE, flags=flags)

    def edited_message(
        self,
        *filters: Filter,
        flags: Optional[Dict[str, Any]] = None,
    ) -> Callable[[Decorated], Decorated]:
        return self.route(*filters, method=UpdateType.EDITED_MESSAGE, flags=flags)

    def channel_post(
        self,
        *filters: Filter,
        flags: Optional[Dict[str, Any]] = None,
    ) -> Callable[[Decorated], Decorated]:
        return self.route(*filters, method=UpdateType.CHANNEL_POST, flags=flags)

    def edited_channel_post(
        self,
        *filters: Filter,
        flags: Optional[Dict[str, Any]] = None,
    ) -> Callable[[Decorated], Decorated]:
        return self.route(*filters, method=UpdateType.EDITED_CHANNEL_POST, flags=flags)

    def inline_query(
        self,
        *filters: Filter,
        flags: Optional[Dict[str, Any]] = None,
    ) -> Callable[[Decorated], Decorated]:
        return self.route(*filters, method=UpdateType.INLINE_QUERY, flags=flags)

    def chosen_inline_result(
        self,
        *filters: Filter,
        flags: Optional[Dict[str, Any]] = None,
    ) -> Callable[[Decorated], Decorated]:
        return self.route(*filters, method=UpdateType.CHOSEN_INLINE_RESULT, flags=flags)

    def callback_query(
        self,
        *filters: Filter,
        flags: Optional[Dict[str, Any]] = None,
    ) -> Callable[[Decorated], Decorated]:
        return self.route(*filters, method=UpdateType.CALLBACK_QUERY, flags=flags)

    def shipping_query(
        self,
        *filters: Filter,
        flags: Optional[Dict[str, Any]] = None,
    ) -> Callable[[Decorated], Decorated]:
        return self.route(*filters, method=UpdateType.SHIPPING_QUERY, flags=flags)

    def pre_checkout_query(
        self,
        *filters: Filter,
        flags: Optional[Dict[str, Any]] = None,
    ) -> Callable[[Decorated], Decorated]:
        return self.route(*filters, method=UpdateType.PRE_CHECKOUT_QUERY, flags=flags)

    def poll(
        self,
        *filters: Filter,
        flags: Optional[Dict[str, Any]] = None,
    ) -> Callable[[Decorated], Decorated]:
        return self.route(*filters, method=UpdateType.POLL, flags=flags)

    def poll_answer(
        self,
        *filters: Filter,
        flags: Optional[Dict[str, Any]] = None,
    ) -> Callable[[Decorated], Decorated]:
        return self.route(*filters, method=UpdateType.POLL_ANSWER, flags=flags)

    def my_chat_member(
        self,
        *filters: Filter,
        flags: Optional[Dict[str, Any]] = None,
    ) -> Callable[[Decorated], Decorated]:
        return self.route(*filters, method=UpdateType.MY_CHAT_MEMBER, flags=flags)

    def chat_member(
        self,
        *filters: Filter,
        flags: Optional[Dict[str, Any]] = None,
    ) -> Callable[[Decorated], Decorated]:
        return self.route(*filters, method=UpdateType.CHAT_MEMBER, flags=flags)

    def chat_join_request(
        self,
        *filters: Filter,
        flags: Optional[Dict[str, Any]] = None,
    ) -> Callable[[Decorated], Decorated]:
        return self.route(*filters, method=UpdateType.CHAT_JOIN_REQUEST, flags=flags)
