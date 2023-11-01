from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "chat_statistic" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "user_id" BIGINT NOT NULL,
    "chat_id" BIGINT NOT NULL,
    "animation_count" BIGINT NOT NULL  DEFAULT 0,
    "audio_count" BIGINT NOT NULL  DEFAULT 0,
    "command_count" BIGINT NOT NULL  DEFAULT 0,
    "contact_count" BIGINT NOT NULL  DEFAULT 0,
    "dice_count" BIGINT NOT NULL  DEFAULT 0,
    "document_count" BIGINT NOT NULL  DEFAULT 0,
    "forward_count" BIGINT NOT NULL  DEFAULT 0,
    "location_count" BIGINT NOT NULL  DEFAULT 0,
    "photo_count" BIGINT NOT NULL  DEFAULT 0,
    "pinned_message_count" BIGINT NOT NULL  DEFAULT 0,
    "poll_count" BIGINT NOT NULL  DEFAULT 0,
    "reaction_count" BIGINT NOT NULL  DEFAULT 0,
    "sticker_count" BIGINT NOT NULL  DEFAULT 0,
    "video_count" BIGINT NOT NULL  DEFAULT 0,
    "voice_count" BIGINT NOT NULL  DEFAULT 0,
    "message_count" BIGINT NOT NULL  DEFAULT 0,
    "word_count" BIGINT NOT NULL  DEFAULT 0,
    "letter_count" BIGINT NOT NULL  DEFAULT 0
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
