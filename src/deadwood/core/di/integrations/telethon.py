from collections.abc import Callable
from functools import wraps
from inspect import Parameter, signature
from typing import Any, Final, ParamSpec, TypeVar

from dishka import AsyncContainer, FromDishka, Provider, Scope, from_context
from dishka.integrations.base import (
    InjectFunc,
    is_dishka_injected,
    wrap_injection,
)
from telethon import TelegramClient, events

__all__ = [
    "CONTAINER_NAME",
    "TelethonProvider",
    "FromDishka",
    "inject",
    "setup_dishka",
]

P = ParamSpec("P")
T = TypeVar("T")
CONTAINER_NAME: Final = "dishka_container"


def inject[**P, T](func: Callable[P, T]) -> Callable[P, T]:
    if CONTAINER_NAME in signature(func).parameters:
        additional_params = []
    else:
        additional_params = [
            Parameter(
                name=CONTAINER_NAME,
                annotation=AsyncContainer,
                kind=Parameter.KEYWORD_ONLY,
            ),
        ]

    return wrap_injection(
        func=func,
        is_async=True,
        additional_params=additional_params,
        container_getter=lambda args, kwargs: kwargs[CONTAINER_NAME],
    )


def setup_dishka[**P, T](
    container: AsyncContainer,
    client: TelegramClient,
    *,
    auto_inject: bool | InjectFunc[P, T] = False,
) -> None:
    original_add_event_handler = client.add_event_handler

    active_inject_func: InjectFunc[P, T]
    if callable(auto_inject):
        active_inject_func = auto_inject
    else:
        active_inject_func = inject

    def _create_wrapped_handler(
        func: Callable[..., Any],
    ) -> Callable[..., Any]:
        if is_dishka_injected(func):
            injected_func = func
        else:
            injected_func = active_inject_func(func)

        is_actually_wrapped = hasattr(injected_func, "__dishka_orig_func__")

        @wraps(func)
        async def handler_wrapper(
            event: Any,
            *args: Any,
            **kwargs: Any,
        ) -> Any:
            context_data = {type(event): event}

            async with container(context=context_data) as request_container:
                if is_actually_wrapped:
                    kwargs[CONTAINER_NAME] = request_container
                return await injected_func(event, *args, **kwargs)

        return handler_wrapper

    def on_wrapper(
        event_builder: Any = None,
        **kwargs: Any,
    ) -> Callable[[Callable[..., Any]], Callable[..., Any]]:

        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            wrapped_func = _create_wrapped_handler(func)
            original_add_event_handler(wrapped_func, event_builder, **kwargs)
            return wrapped_func

        return decorator

    def add_event_handler_wrapper(
        func: Callable[..., Any],
        event_builder: Any = None,
        **kwargs: Any,
    ) -> None:
        if getattr(func, "_dishka_wrapped", False):
            original_add_event_handler(func, event_builder, **kwargs)
        else:
            wrapped_func = _create_wrapped_handler(func)
            wrapped_func._dishka_wrapped = True  # type: ignore
            original_add_event_handler(wrapped_func, event_builder, **kwargs)

    client.on = on_wrapper
    client.add_event_handler = add_event_handler_wrapper


class TelethonProvider(Provider):
    message = from_context(
        provides=events.NewMessage.Event,
        scope=Scope.REQUEST,
    )

    event = from_context(
        provides=events.Raw,
        scope=Scope.REQUEST,
    )
