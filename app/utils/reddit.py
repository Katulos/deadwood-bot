import aiohttp
import asyncpraw
import asyncprawcore

from app import shared


class RedditWrapper:
    def __init__(self) -> None:
        self.session = aiohttp.ClientSession()
        self.reddit = asyncpraw.Reddit(
            client_id=shared.settings.REDDIT_ID,
            client_secret=shared.settings.REDDIT_SECRET,
            user_agent="Trenddit/0.0.2",
            refresh_token=shared.settings.REDDIT_TOKEN,
        )
        self.reddit.read_only = True

    async def fetch(self, keywords):
        args = keywords.split()
        sub = args[0]
        if len(args) > 1:
            kwds = "+".join(args[1:])
        else:
            kwds = ""
        try:
            subs = await self._get_list(sub, kwds)
        except asyncprawcore.OAuthException:
            subs = await self._get_list(sub, kwds)
        await self._close_connection()
        return subs

    async def _get_list(self, sub, keywords):
        try:
            if keywords:
                subreddit = await self.reddit.subreddit(sub)
                search = subreddit.search(
                    keywords,
                    sort="top",
                    limit=500,
                    params={"include_over_18": "on"},
                )
                data = [[u.title, u.url] async for u in search]
                if not data:
                    await self._close_connection()
                    kwds = " ".join(keywords.split("+"))
                    raise RedditException(
                        f"Nothing found in subreddit '{sub}'"
                        f" with keywords '{kwds}'",
                    )
            else:
                subreddit = await self.reddit.subreddit(sub)
                data = [
                    [u.title, u.url]
                    async for u in subreddit.top(limit=500)
                ]
                if not data:
                    await self._close_connection()
                    raise RedditException(
                        f"Looks like subreddit '{sub}' is empty",
                    )
        except asyncprawcore.NotFound as e:
            raise RedditException(f"Subreddit '{sub}' not found") from e
        except asyncprawcore.Forbidden as e:
            raise RedditException(f"Subreddit '{sub}' is private") from e
        except asyncprawcore.Redirect as e:
            raise RedditException(
                f"Looks like subreddit '{sub}' is empty",
            ) from e
        except asyncprawcore.BadRequest as e:
            raise RedditException("Something went wrong, try again") from e
        return await self._get_elements(data)

    async def _get_elements(self, links: list):
        data = []
        for title, url in links:
            if url.endswith(
                (
                    ".jpg",
                    ".jpeg",
                    ".png",
                    ".gif",
                    ".mp4",
                    ".gifv",
                    ".webm",
                    ".webp",
                ),
            ):
                if url.endswith(".gifv"):
                    url = url.replace(".gifv", ".mp4")
                data.append([url, title])
        if not data:
            raise RedditException(
                "Looks like subreddit is empty",
            )
        return data

    async def _close_connection(self):
        await self.reddit.close()
        await self.session.close()


class RedditException(Exception):
    pass
