from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "chat" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "chat_id" BIGINT NOT NULL UNIQUE,
    "chat_title" VARCHAR(128) NOT NULL DEFAULT 'False',
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "chat_flag" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "enabled" INT NOT NULL DEFAULT 0,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "chat_id" BIGINT NOT NULL UNIQUE REFERENCES "chat" ("id") ON DELETE CASCADE
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


MODELS_STATE = (
    "eJztmO9P4jAYx/8Vwisv8QwOEO7eDcSTi8JF8e6iMUvZymjsWty6U2L436/tVrYVNkGihx"
    "5vCHt+bH0+T7t+16eyB4eUHbTHgJW/lp7KBHiQ/0mb90tlMJnMjeKagSGWYbYKGAbMB7a4"
    "xwjgAHKTAwPbRxOGKOFWEmIsjNTmgYi4iSkk6D6EFqMuZGPoc8fNLTcj4sBHGKjLyZ01Qh"
    "A7mUEiRzxb2i02nUhbC7ldwk5krHjg0LIpDj2SxE+mbEzJPAERWYELCfQBg+IJzA9FBWKA"
    "caGqqGiwSUg0ylSOA0cgxCxV8YoYbEoEQj6aQNboiqd8/mIY1WrDqFSPmvVao1FvVpo8Vg"
    "5p0dWYRQUnQKJbSSzdb93eQBRKeZ+i5gnDTOYABqIsyTsBLNprrUs5lfQ8agX2f2GtsWWI"
    "cf8CXr7u/AK48yyNLy/qJXyVIQGcrGFFeN1VrSP2wKOFIXHZmF8eGs0CfD/Ni/apebHHoz"
    "5lIfZilxH5NJ4+FDVb0Qspy/OYexjyYA7TTKbG1IlTD9Sf1yK84RzmNTh9gqfx8ijgO+ie"
    "dy4H5vkPUYkXBPdYIjIHHeExpHWqWfeOtFbMb1L61R2clsRl6brf60iCNGCuL5+YxA2uy2"
    "JMIGTUIvTBAk5qJSurApNpbDhxXtjYbOausf+0sXLwYisf3aX2GmEYAvvuAfiOteChBs2L"
    "zbqS2TLCwA2WbFhxXp/AAeU/FxAD2YrFiZFInxN+rxVmRVzrG06KmZrpyprm6xmeBs0DBL"
    "hyIOJ2IlmrcbnyU+UXqj9rpKJ2EvD9ypJ8CQiJqH8ZZUoxBGQ55lSWxnrI07ZUpBSx6/fP"
    "Mm/VVlcj2bs6b3W4aJGvUx6EWJ7u2+mUj7Cd7XTKB21sPPjdR/Br7TYbacBsWxZ7ovSd7E"
    "qXVwiIvexTOXu+tW3NyNN33OyDh7kMSs8yXpsDMYx2nbZ52TaPO+VZgWReTyqa0Ef2eIlQ"
    "jB1FMhEkIVujET+QQDQOa41as3pUm6/UuaVogT4v/f5AP4g/kVY9nkqlvN3Z1IYUM0dTRr"
    "2+wtEUj8o9mpK+rOQTK2MNiHH4+wR4WKmscrZXqeSf7QmfppkpYZAsed1/v+z3cjbgJEUD"
    "eUV4gTcOstl+CaOA3W4n1gKKouqMdlLw9s7N3zrX9lm/pYsicYPWplvxpnvL7C/Ai2u3"
)
