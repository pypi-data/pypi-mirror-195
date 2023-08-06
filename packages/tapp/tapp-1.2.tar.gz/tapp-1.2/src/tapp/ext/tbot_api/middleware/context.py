from typing import Any, Awaitable, Callable, Dict, Optional, Tuple

from tbot_api.types import Chat, TelegramObject, Update, User

from ....middleware import BaseMiddleware


def resolve(update: Update) -> Tuple[Optional[Chat], Optional[User]]:
    if update.message:
        return update.message.chat, update.message.from_user
    if update.edited_message:
        return update.edited_message.chat, update.edited_message.from_user
    if update.channel_post:
        return update.channel_post.chat, None
    if update.edited_channel_post:
        return update.edited_channel_post.chat, None
    if update.inline_query:
        return None, update.inline_query.from_user
    if update.chosen_inline_result:
        return None, update.chosen_inline_result.from_user
    if update.callback_query:
        if update.callback_query.message:
            return update.callback_query.message.chat, update.callback_query.from_user
        return None, update.callback_query.from_user
    if update.shipping_query:
        return None, update.shipping_query.from_user
    if update.pre_checkout_query:
        return None, update.pre_checkout_query.from_user
    if update.poll_answer:
        return None, update.poll_answer.from_user
    if update.my_chat_member:
        return update.my_chat_member.chat, update.my_chat_member.from_user
    if update.chat_member:
        return update.chat_member.chat, update.chat_member.from_user
    if update.chat_join_request:
        return update.chat_join_request.chat, update.chat_join_request.from_user
    return None, None


class ContextMiddleware(BaseMiddleware):
    async def __call__(
        self,
        route: Callable[[Any, Dict[str, Any]], Awaitable[None]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        update = data["original_update"]

        chat, user = resolve(update=update)
        if chat:
            data["event_chat"] = chat
        if user:
            data["event_user"] = user
        return await route(event, data)
