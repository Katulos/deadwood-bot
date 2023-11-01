import asyncio
import random

from pyrogram import Client, enums, errors, filters
from pyrogram.types import Message
from tortoise.functions import Sum

from app import _, logger, ngettext
from app.bot import command
from app.models import ChatStatistic


# pylint: disable=no-member
@Client.on_message(command(["stat"]) & (filters.group | filters.private))
async def stat_command_handler(client: Client, message: Message) -> None:
    try:
        reply_to = (
            message.reply_to_message.from_user.id
            if message.reply_to_message
            else message.from_user.id
        )
        mention = (
            message.reply_to_message.from_user.mention
            if message.reply_to_message
            else message.from_user.mention
        )
        stat = await ChatStatistic.filter(
            chat_id=message.chat.id,
            user_id=reply_to,
        ).annotate(
            animations=Sum("animation_count"),
            audios=Sum("audio_count"),
            forwards=Sum("forward_count"),
            photos=Sum("photo_count"),
            stickers=Sum("sticker_count"),
            videos=Sum("video_count"),
            voices=Sum("voice_count"),
            messages=Sum("message_count"),
            words=Sum("word_count"),
            letters=Sum("letter_count"),
        )
        await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
        await asyncio.sleep(random.randint(3, 6))

        if stat[0].id is None:  # wtf?
            msg = await message.reply(_("No statistics available"))
        else:
            msg = await message.reply(
                _("`----- [ Statistic` **%(mention)s**` ] -----`\n")
                % {"mention": mention}
                + ngettext(
                    "\U0001f39e **%(animations)d** `animation`\n",
                    "\U0001f39e **%(animations)d** `animations`\n",
                    stat[0].animations,
                )
                % {"animations": stat[0].animations}
                + ngettext(
                    "\U0001f3a7 **%(audios)d** `audio`\n",
                    "\U0001f3a7 **%(audios)d** `audios`\n",
                    stat[0].audios,
                )
                % {"audios": stat[0].audios}
                + ngettext(
                    "\U000023E9 **%(forwards)d** `forward`\n",
                    "\U000023E9 **%(forwards)d** `forwards`\n",
                    stat[0].forwards,
                )
                % {"forwards": stat[0].forwards}
                + ngettext(
                    "\U0001f5bc **%(photos)d** `photo`\n",
                    "\U0001f5bc **%(photos)d** `photos`\n",
                    stat[0].photos,
                )
                % {"photos": stat[0].photos}
                + ngettext(
                    "\U0001f3f7 **%(stickers)d** `sticker`\n",
                    "\U0001f3f7 **%(stickers)d** `stickers`\n",
                    stat[0].stickers,
                )
                % {"stickers": stat[0].stickers}
                + ngettext(
                    "\U0001f4fd **%(videos)d** `video`\n",
                    "\U0001f4fd **%(videos)d** `videos`\n",
                    stat[0].videos,
                )
                % {"videos": stat[0].videos}
                + ngettext(
                    "\U0001f399 **%(voices)d** `voice`\n",
                    "\U0001f399 **%(voices)d** `voices`\n",
                    stat[0].voices,
                )
                % {"voices": stat[0].voices}
                + ngettext(
                    "\U0001f4e3 **%(messages)d** `message`\n",
                    "\U0001f4e3 **%(messages)d** `messages`\n",
                    stat[0].messages,
                )
                % {"messages": stat[0].messages}
                + ngettext(
                    "\U0001f4ac **%(words)d** `word`\n",
                    "\U0001f4ac **%(words)d** `words`\n",
                    stat[0].words,
                )
                % {"words": stat[0].words}
                + ngettext(
                    "\U0001f18e **%(letters)d** `letter`\n",
                    "\U0001f18e **%(letters)d** `letters`\n",
                    stat[0].letters,
                )
                % {"letters": stat[0].letters}
                + "`----- [ EOF ] -----`",
            )
        await asyncio.sleep(random.randint(10, 20))
        await client.delete_messages(
            chat_id=message.chat.id,
            message_ids=[msg.id, message.id],
        )
    except errors.MessageDeleteForbidden as e:
        logger.error(e)
