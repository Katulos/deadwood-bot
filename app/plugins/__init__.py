import asyncio
import importlib
import inspect
import os
import time
from collections.abc import Coroutine, Generator
from typing import Any, Optional

import structlog

from app.utils import logging

logger: structlog.typing.FilteringBoundLogger = logging.setup_logger().bind(
    type="business",
)


async def init(client: Any) -> None:
    plugins = [
        importlib.import_module(".", f"{__name__}.{file[:-3]}")
        for file in os.listdir(os.path.dirname(__file__))
        if file[0].isalpha() and file.endswith(".py")
    ]

    modules: dict[str, Any] = {m.__name__.split(".")[-1]: m for m in plugins}

    to_init: Generator[Optional[Coroutine[Any, Any, None]], None, None] = (
        get_init_coro(plugin, client=client, modules=modules)
        for plugin in plugins
    )

    await asyncio.gather(*(coro for coro in to_init if coro is not None))


def get_init_coro(
    plugin: Any,
    **kwargs: Any,
) -> Optional[Coroutine[Any, Any, None]]:
    p_init = getattr(plugin, "init", None)
    if not callable(p_init):
        return None

    result_kwargs: dict[str, Any] = {}
    sig = inspect.signature(p_init)
    for param in sig.parameters:
        if param in kwargs:
            result_kwargs[param] = kwargs[param]
        else:
            param_name = str(param)
            logger.error(
                "Plugin %s has unknown init parameter %s",
                plugin.__name__,
                param_name,
            )
            return None

    return _init_plugin(plugin, result_kwargs)


async def _init_plugin(plugin: Any, kwargs: dict[str, Any]) -> None:
    try:
        logger.info(f"Loading plugin {plugin.__name__}…")
        start = time.time()
        ret = await plugin.init(**kwargs)
        took = time.time() - start
        logger.info(f"Loaded plugin {plugin.__name__} (took {took:.2f}s)")
        if asyncio.iscoroutine(ret):
            await ret
    except Exception:
        logger.exception(f"Failed to load plugin {plugin.__name__}")


async def start_plugins(client: Any, plugins: list[Any]) -> None:
    await asyncio.gather(
        *(_init_plugin(client, plugin) for plugin in plugins),
    )
