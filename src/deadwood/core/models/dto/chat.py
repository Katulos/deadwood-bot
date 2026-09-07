from datetime import datetime

from attr import dataclass


@dataclass
class Chat:
    chat_id: int
    chat_title: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
