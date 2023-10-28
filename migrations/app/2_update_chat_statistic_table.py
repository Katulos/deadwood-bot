from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    # sqlite specific
    return """
        ALTER TABLE "chat_statistic" ADD "updated_at" TIMESTAMP;
        UPDATE "chat_statistic" SET "updated_at" = CURRENT_TIMESTAMP;
        ALTER TABLE "chat_statistic" ADD "created_at" TIMESTAMP;
        UPDATE "chat_statistic" SET "created_at" = CURRENT_TIMESTAMP;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
