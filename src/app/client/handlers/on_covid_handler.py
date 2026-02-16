from telethon import TelegramClient, events, functions
from telethon.tl.custom import Message
from telethon.tl.types import SendMessageUploadPhotoAction

from app.core.config import settings

_pattern = r"(?i).*\b(.*covid.*|.*коронав.*|.*пандеми.*|.*ковид.*)\b"


async def init(client: TelegramClient):
    @client.on(
        events.NewMessage(
            pattern=_pattern,
            func=lambda e: e.is_group,
        ),
    )
    async def on_covid_handler(event: Message):
        # TODO: implement this
        # chat = (
        #     await Chat.filter(chat_id=event.chat.id)
        #     .prefetch_related("flags")
        #     .get_or_none()
        # )
        # if not chat.flags.enabled:
        #     return
        static_path = settings.get("static_path")

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
            file=static_path + "/reactions/covid.png",
            reply_to=event.message.id,
        )
