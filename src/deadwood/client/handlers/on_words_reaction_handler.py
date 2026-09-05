import random
import re
from typing import Any

from telethon import TelegramClient, events, functions
from telethon.errors import UserAdminInvalidError
from telethon.tl.custom import Message
from telethon.tl.functions.messages import (
    GetStickerSetRequest,
)
from telethon.tl.types import (
    InputStickerSetShortName,
    SendMessageUploadPhotoAction,
)

from deadwood.utils import get_mention, parse_time

_covid_pattern = re.compile(
    r"(?i).*\b(.*covid.*|.*коронав.*|.*пандеми.*|.*ковид.*)\b",
)

_owner_pattern = re.compile(
    r"(?i).*\b(.*котосос.*|.*к[ао]т[ао]лу.*|.*котоло.*|.*ĸотолу.*|.*к[ао]к[ао]лус.*|.*к[ао]кул[оа]с.*|.*всратул.*|.*vsratu.*)\b",
)


async def init(client: TelegramClient) -> None:
    stickerset = await client(
        GetStickerSetRequest(InputStickerSetShortName("dead_bot"), hash=0),
    )
    documents = stickerset.documents

    @client.on(  # type: ignore[untyped-decorator]
        events.NewMessage(
            pattern=_covid_pattern,
            func=lambda e: e.is_group,
        ),
    )
    async def on_covid_handler(event: Message) -> None:
        # TODO: implement this
        # chat = (
        #     await Chat.filter(chat_id=event.chat.id)
        #     .prefetch_related("flags")
        #     .get_or_none()
        # )
        # if not chat.flags.enabled:
        #     return

        await client(
            functions.messages.SetTypingRequest(
                peer=event.chat.id,
                action=SendMessageUploadPhotoAction(
                    progress=5,  # why 5?
                ),
            ),
        )
        await client.send_file(
            event.chat.id,
            file=documents[2],  # cat in pants
            reply_to=event.message.id,
        )

    @client.on(  # type: ignore[untyped-decorator]
        events.NewMessage(
            pattern=_owner_pattern,
            func=lambda e: e.is_group,
        ),
    )
    async def on_ovner_handler(event: Message) -> None:
        # TODO: implement this
        # chat = (
        #     await Chat.filter(chat_id=event.chat.id)
        #     .prefetch_related("flags")
        #     .get_or_none()
        # )
        # if not chat.flags.enabled:
        #     return
        says_variant = {
            0: 0.1,
            1: 99.9,
        }
        say = _get_weighted_rand(says_variant)
        match say:
            case 0:
                try:
                    await client.edit_permissions(
                        event.chat.id,
                        event.sender.id,
                        until_date=parse_time("1m"),
                        send_messages=False,
                    )
                    await event.respond(
                        get_mention(event.sender) + " muted for 1 minute",
                        parse_mode="HTML",
                    )
                except UserAdminInvalidError:
                    await client.send_file(
                        event.chat.id,
                        file=documents[44],
                        reply_to=(
                            event.message.reply_to_msg_id
                            if event.message.reply_to_msg_id
                            else event.message.id
                        ),
                    )
            case 1:
                await client.send_file(
                    event.chat.id,
                    file=documents[45],
                    reply_to=(
                        event.message.reply_to_msg_id
                        if event.message.reply_to_msg_id
                        else event.message.id
                    ),
                )
                # ping @vskopuk
                await event.respond(
                    "Wake up [Neo](tg://user?id=211930163)...\nYou obosralsya.",
                    reply_to=(
                        event.message.reply_to_msg_id
                        if event.message.reply_to_msg_id
                        else event.message.id
                    ),
                )
            case _:
                pass

    def _get_weighted_rand(a: dict[Any, int | float], p: int = 0) -> Any:
        if sum(a.values()) > 100:
            return False

        p_multiplier: int = 10 ** (p + 2)
        n: float = random.randint(1, p_multiplier) * (100 / p_multiplier)

        range_val: float = 100
        for k, v in a.items():
            range_val -= v
            if n > range_val:
                return k

        return list(a.keys())[-1]
