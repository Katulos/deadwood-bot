from io import BytesIO

from pyrogram import Client, filters
from pyrogram.types import Message

from app.bot import command


@Client.on_message(
    command(["json"]) & (filters.group | filters.private),
)
async def json_command_handler(client: Client, message: Message) -> None:
    msg = message.reply_to_message if message.reply_to_message else message
    if len(str.encode(str(msg))) > 4096:
        with BytesIO(str.encode(str(msg))) as file:
            file.name = "json.txt"
            await client.send_document(
                chat_id=message.chat.id,
                reply_to_message_id=message.id,
                document=file,
                protect_content=True,
            )
    else:
        await message.reply(f"<pre>{msg}</pre>", protect_content=True)
