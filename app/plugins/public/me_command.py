import re

from pyrogram import Client, filters
from pyrogram.types import Message

from app.bot import command

me_command = "me"


# pylint: disable=no-member
@Client.on_message(
    command([me_command]) & (filters.group | filters.private),
)
async def me_command_handler(client: Client, message: Message) -> None:
    pattern = rf"(?i)^[/!\\.]{me_command} (.*?)$"
    if re.match(pattern, message.text):
        me = await client.get_chat_member(message.chat.id, client.me.id)
        if me.privileges.can_delete_messages:
            s = message.text[4:]
            await message.delete()
            if message.reply_to_message:
                await message.reply(
                    f"* <b>{message.from_user.mention}</b> {s}",
                    reply_to_message_id=message.reply_to_message_id,
                    protect_content=True,
                )
            else:
                await client.send_message(
                    message.chat.id,
                    f"* <b>{message.from_user.mention}</b> {s}",
                    protect_content=True,
                )
        else:
            return
    else:
        return
