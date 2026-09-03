from dishka import AsyncContainer, make_async_container


def get_async_container() -> AsyncContainer:
    providers = []
    container = make_async_container(*providers)
    return container
