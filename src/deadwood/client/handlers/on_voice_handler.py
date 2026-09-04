import asyncio
import logging
from random import randint

from telethon import TelegramClient, events, functions
from telethon.tl.custom import Message
from telethon.tl.types import (
    SendMessageRecordAudioAction,
    SendMessageTypingAction,
    SendMessageUploadVideoAction,
)

from deadwood.core import settings


async def init(client: TelegramClient) -> None:
    @client.on(  # type: ignore[untyped-decorator]
        events.NewMessage(func=lambda e: e.is_group and e.message.voice),
    )
    async def on_voice_handler(event: Message) -> None:
        # TODO: implement this
        # chat = (
        #     await Chat.filter(chat_id=event.chat.id)
        #     .prefetch_related("flags")
        #     .get_or_none()
        # )
        # if not chat.flags.enabled:
        #     return
        static_path = settings.get("static_path")
        random_int = randint(1, 4)

        await asyncio.sleep(random_int)

        match random_int:
            case 1:
                await client(
                    functions.messages.SetTypingRequest(
                        peer=event.chat.id,
                        action=SendMessageRecordAudioAction(),
                    ),
                )
                await client.send_file(
                    event.chat.id,
                    file=static_path
                    + "/reactions/no-voice-message-alla1.ogg",
                    reply_to=event.message.id,
                    voice_note=True,
                )
            case 2:
                await client(
                    functions.messages.SetTypingRequest(
                        peer=event.chat.id,
                        action=SendMessageRecordAudioAction(),
                    ),
                )
                await client.send_file(
                    event.chat.id,
                    file=static_path
                    + "/reactions/no-voice-message-alla2.ogg",
                    reply_to=event.message.id,
                    voice_note=True,
                )
            case 3:
                await client(
                    functions.messages.SetTypingRequest(
                        peer=event.chat.id,
                        action=SendMessageUploadVideoAction(
                            progress=5,  # why?
                        ),
                    ),
                )
                await client.send_file(
                    event.chat.id,
                    file=static_path + "/reactions/no-voice-message.mp4",
                    reply_to=event.message.id,
                )
            case 4:
                await client(
                    functions.messages.SetTypingRequest(
                        peer=event.chat.id,
                        action=SendMessageTypingAction(),
                    ),
                )
                await event.reply("Voice whore is not a human")
            case _:
                await client(
                    functions.messages.SetTypingRequest(
                        peer=event.chat.id,
                        action=SendMessageTypingAction(),
                    ),
                )
                await event.reply("Voice whore is not a human")
                logging.error("Unknown random int")
