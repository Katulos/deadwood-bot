from html import escape
from typing import Any, Callable, Union, cast

import orjson
from telethon.tl.types import User


def get_mention(user: User) -> str:
    name = escape(user.first_name or "Some asshole with a crooked nickname")
    if user.last_name:
        name += f" {escape(user.last_name)}"
    return f'<a href="tg://user?id={user.id}">{name}</a>'


def orjson_dumps(
    v: Any,
    *,
    default: Union[Callable[[Any], Any], None],
) -> str:
    result = orjson.dumps(v, default=default).decode()
    return cast(str, result)
