import asyncio
from random import randint

from pyrogram import Client, enums, filters
from pyrogram.types import Message

from app import _, shared


@Client.on_message(filters.voice & (filters.group | filters.private))
async def on_voice_handler(client: Client, message: Message):
    static_path = shared.settings.STATIC_PATH
    random_int = randint(1, 4)
    if random_int == 1:
        await client.send_chat_action(
            message.chat.id,
            enums.ChatAction.RECORD_AUDIO,
        )
        await asyncio.sleep(random_int)
        await client.send_voice(
            chat_id=message.chat.id,
            voice=static_path + "/reactions/no-voice-message-alla1.ogg",
            protect_content=True,
            reply_to_message_id=message.id,
        )
    elif random_int == 2:
        await client.send_chat_action(
            message.chat.id,
            enums.ChatAction.RECORD_AUDIO,
        )
        await asyncio.sleep(random_int)
        await client.send_voice(
            chat_id=message.chat.id,
            voice=static_path + "/reactions/no-voice-message-alla1.ogg",
            protect_content=True,
            reply_to_message_id=message.id,
        )
    elif random_int == 3:
        await client.send_chat_action(
            message.chat.id,
            enums.ChatAction.RECORD_VIDEO,
        )
        await asyncio.sleep(random_int)
        await client.send_video_note(
            chat_id=message.chat.id,
            video_note=static_path + "/reactions/no-voice-message.mp4",
            protect_content=True,
            reply_to_message_id=message.id,
        )
    else:
        await client.send_chat_action(
            message.chat.id,
            enums.ChatAction.TYPING,
        )
        await asyncio.sleep(random_int)
        await message.reply(_("Voice whore is not a human"))
