import random

from telethon import TelegramClient
from telethon.errors import UserAdminInvalidError
from telethon.tl.custom import Message
from telethon.tl.functions.messages import (
    GetStickerSetRequest,
)
from telethon.tl.types import (
    InputStickerSetShortName,
)

from deadwood.client.decorators import command
from deadwood.utils import get_mention, parse_time

dice_command = "dice"


async def init(client: TelegramClient) -> None:
    stickerset = await client(
        GetStickerSetRequest(InputStickerSetShortName("dicenew"), hash=0),
    )
    documents = stickerset.documents

    @command(dice_command)  # type: ignore[untyped-decorator]
    async def dice_command_handler(event: Message) -> None:
        num = _dice_random_choice()

        match num:
            case 0:
                try:
                    await client.edit_permissions(
                        event.chat.id,
                        event.sender.id,
                        until_date=parse_time("1m"),
                        send_messages=False,
                    )
                    await client.send_file(
                        event.chat.id,
                        file=documents[num],
                        reply_to=event.message.id,
                    )
                    await event.respond(
                        get_mention(event.sender) + " banned for 1 minute",
                        parse_mode="HTML",
                    )
                except UserAdminInvalidError:
                    await client.send_file(
                        event.chat.id,
                        file=documents[num],
                        reply_to=event.message.id,
                    )
                    await event.respond(
                        "You got a BAN, but I'm not right enough",
                        parse_mode="HTML",
                    )
            case 9:
                await client.send_file(
                    event.chat.id,
                    file=documents[num],
                    reply_to=event.message.id,
                )
                mention = get_mention(event.sender)
                await event.respond(
                    f"Yep {mention}, you're a faggot!",
                    parse_mode="HTML",
                )
            case _:
                await client.send_file(
                    event.chat.id,
                    file=documents[num],
                    reply_to=event.message.id,
                )

    def _dice_random_choice() -> int:
        w = [0, 2, 3, 4, 5, 6, 7, 9]
        p = [0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.02]
        num = random.choices(w, weights=p, k=1)[0]
        return num
