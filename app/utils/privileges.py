async def is_admin(chat_id: int, user_id: int) -> bool:
    raise NotImplementedError


async def is_bot(chat_id: int, user_id: int) -> bool:
    raise NotImplementedError


async def is_enabled_command(chat_id: int, command: list[str]) -> bool:
    return True
    # raise NotImplementedError
