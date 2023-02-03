import asyncio

from pyrogram import Client, enums, errors, filters
from pyrogram.types import Message

from app import _, logger

pattern = r"(?i).*\b(.*covid.*|.*коронав.*|.*пандеми.*|.*ковид.*)\b"


@Client.on_message(filters.regex(pattern) & (filters.group | filters.private))
async def on_covid_handler(client: Client, message: Message):
    await client.send_chat_action(
        message.chat.id,
        enums.ChatAction.UPLOAD_PHOTO,
    )
    await asyncio.sleep(2)
    try:
        await client.send_photo(
            chat_id=message.chat.id,
            photo="https://i.imgur.com/2fKr5Gi.png",
            protect_content=True,
            reply_to_message_id=message.id,
        )
    except errors.WebpageCurlFailed as e:
        message.reply(_("Great news! You have COVID!"))
        logger.error(e)
    except errors.MediaEmpty as e:
        message.reply(_("Great news! You have COVID!"))
        logger.error(e)
