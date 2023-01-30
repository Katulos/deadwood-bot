from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "chat" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "name" VARCHAR(128) NOT NULL  DEFAULT 'False',
    "last_admins_update" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "chat_member" (
    "user_id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "chat_id" BIGINT NOT NULL,
    "is_admin" INT NOT NULL  DEFAULT 0,
    "is_bot" INT NOT NULL  DEFAULT 0,
    "is_banned" INT NOT NULL  DEFAULT 0
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
