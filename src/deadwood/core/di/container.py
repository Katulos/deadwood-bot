from dishka import AsyncContainer, Provider, make_async_container


def get_async_container() -> AsyncContainer:
    providers: list[Provider] = []
    container = make_async_container(*providers)
    return container
