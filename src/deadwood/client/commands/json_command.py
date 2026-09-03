import asyncio
import logging
import random
from io import BytesIO

import orjson
from telethon import TelegramClient, functions
from telethon.errors import MessageDeleteForbiddenError
from telethon.tl.custom import Message
from telethon.tl.types import (
    SendMessageTypingAction,
    SendMessageUploadDocumentAction,
)

from deadwood.client.decorators import command

json_command = "json"


async def init(client: TelegramClient):
    @command(json_command)
    async def json_command_handler(event: Message):
        try:
            target_msg = (
                await event.message.get_reply_message()
                if event.message.is_reply
                else event.message
            )
            if not target_msg:
                return

            clean_data = _to_serializable(target_msg)
            msg_bytes = orjson.dumps(clean_data, option=orjson.OPT_INDENT_2)
            msg_json = msg_bytes.decode("utf-8")

            is_large = len(msg_json) > 4096
            action = (
                SendMessageUploadDocumentAction(progress=0)
                if is_large
                else SendMessageTypingAction()
            )

            await client(
                functions.messages.SetTypingRequest(
                    peer=event.chat_id,
                    action=action,
                ),
            )

            await asyncio.sleep(random.randint(3, 6))

            if is_large:
                json_file = BytesIO(msg_bytes)
                json_file.name = "message.txt"
                msg = await client.send_file(
                    event.chat_id,
                    json_file,
                    reply_to=event.id,
                )
            else:
                msg = await event.reply(f"```\n{msg_json}\n```")

            await asyncio.sleep(random.randint(10, 20))
            await client.delete_messages(
                event.chat_id,
                message_ids=[msg.id, event.id],
            )

        except MessageDeleteForbiddenError:
            logging.warning("Grant permission can_delete_messages!")
        except Exception as e:
            logging.error(e)

    def _to_serializable(obj):
        if hasattr(obj, "to_dict"):
            return obj.to_dict()
        elif isinstance(obj, dict):
            return {k: _to_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list | tuple):
            return [_to_serializable(i) for i in obj]
        elif isinstance(obj, str | int | float | bool) or obj is None:
            return obj
        else:
            return str(obj)
