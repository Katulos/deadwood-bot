from collections.abc import Coroutine
from functools import wraps
from typing import (
    Any,
    Callable,
    Optional,
    TypeVar,
    Union,
    cast,
)

from telethon import events
from telethon.errors import ChatAdminRequiredError
from telethon.tl.types import Message, User

from app import client
from app.utils import logging
from app.utils.i18n import _
from app.utils.privileges import is_admin, is_enabled_command
from app.utils.tools import get_mention

T = TypeVar("T")
F = TypeVar("F", bound=Callable[..., Coroutine[Any, Any, Any]])
_logger = logging.setup_logger().bind(type="business")


def _validate_command(command: Union[list[str], str]) -> str:
    if isinstance(command, list):
        return "|".join(command)
    return command


def _create_pattern(command: str, with_args: bool = False) -> str:
    base_pattern = rf"(?i)^[./!]({command})(?:@\w+)?"
    return f"{base_pattern} (.*?)$" if with_args else f"{base_pattern}$"


def _handle_command_errors(
    func: Callable[..., Coroutine[Any, Any, Optional[T]]],
) -> Callable[..., Coroutine[Any, Any, Optional[T]]]:
    @wraps(func)
    async def wrapper(
        event: Message,
        *args: Any,
        **kwargs: Any,
    ) -> Optional[T]:
        try:
            return await func(event, *args, **kwargs)
        except ChatAdminRequiredError as e:
            _logger.error(f"Error in command handler: {e}")
            await event.reply(_("not-enough"))
            return None
        except TypeError as e:
            _logger.error(f"Error in command handler: {e}")
            await event.reply(_("something-wrong"))
            return None
        except Exception as e:
            _logger.error(f"Error in command handler: {e}")
            await event.reply(_("something-wrong"))
            return None

    return wrapper


def command_decorator_factory(
    with_args: bool = False,
    admin_only: bool = False,
    moderate: bool = False,
) -> Callable[[Union[list[str], str]], Callable[[F], F]]:
    def decorator(command: Union[list[str], str]) -> Callable[[F], F]:
        def wrapper(func: F) -> F:
            formatted_cmd = _validate_command(command)
            pattern = _create_pattern(formatted_cmd, with_args)

            @client.client.on(
                events.NewMessage(
                    pattern=pattern,
                    func=lambda event: event.is_group,
                ),
            )  # type: ignore
            @_handle_command_errors
            @wraps(func)
            async def handler(event: Message) -> Any:
                if not event.sender:
                    await event.reply(_("to-yourself"))
                    return

                if admin_only and not await is_admin(
                    event.chat.id,
                    event.sender.id,
                ):
                    await event.reply(_("not-enough"))
                    return

                if not admin_only:
                    try:
                        cmd_list = (
                            [command] if isinstance(command, str) else command
                        )
                        if not await is_enabled_command(
                            chat_id=event.chat.id,
                            command=cmd_list,
                        ):
                            return
                    except KeyError as e:
                        _logger.error("Command %s not found in database", e)
                        return

                if moderate:
                    if not event.is_reply:
                        await event.reply(_("doesnt-work-like-that"))
                        return

                    reply_to = await event.get_reply_message()
                    if not reply_to or not reply_to.sender:
                        return

                    if reply_to.sender.bot:
                        await event.reply(_("doesnt-work-like-that"))
                        return

                    if await is_admin(event.chat.id, reply_to.sender.id):
                        await event.reply(_("not-enough"))
                        return

                    result = await func(
                        event.chat.id,
                        reply_to.sender_id,
                        get_mention(cast(User, reply_to.sender)),
                    )
                    await event.respond(result)
                    return

                if with_args:
                    if match := event.pattern_match:
                        return await func(event, cast(str, match.group(2)))
                    return None

                return await func(event)

            return cast(F, handler)

        return wrapper

    return decorator


user_command = command_decorator_factory(with_args=False)
user_par_command = command_decorator_factory(with_args=True)
admin_command = command_decorator_factory(admin_only=True)
admin_par_command = command_decorator_factory(admin_only=True, with_args=True)
moderate_command = command_decorator_factory(admin_only=True, moderate=True)
