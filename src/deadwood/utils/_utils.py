import re
from datetime import timedelta

from telethon.tl.types import User


def get_mention(user: User) -> str:
    name = user.first_name or ""
    if user.last_name:
        name += f" {user.last_name}"
    if not name:
        name = "Asshole with a crooked nickname"

    return f'<a href="tg://user?id={user.id}">{name}</a>'


def parse_time(time_str: str) -> timedelta | None:
    parse_time_regex = re.compile(
        r"((?P<hours>\d+?)hr)?((?P<minutes>\d+?)m)?((?P<seconds>\d+?)s)?",
    )
    match = parse_time_regex.match(time_str)
    if not match:
        return None

    parts = match.groupdict()
    time_params: dict[str, int] = {}
    for name, param in parts.items():
        if param:
            time_params[name] = int(param)

    return timedelta(**time_params)
