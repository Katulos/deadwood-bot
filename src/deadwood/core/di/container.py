from dishka import AsyncContainer, Provider, make_async_container

from deadwood.core.di.providers.db import DAOProvider, DbProvider

from .integrations.telethon import TelethonProvider


def get_async_container() -> AsyncContainer:
    providers: list[Provider] = [
        DbProvider(),
        DAOProvider(),
        TelethonProvider(),
    ]
    container = make_async_container(*providers)
    return container
