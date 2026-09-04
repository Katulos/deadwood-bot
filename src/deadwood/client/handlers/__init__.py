import asyncio
import importlib
import inspect
import logging
import os
import time
from collections.abc import Coroutine
from types import ModuleType
from typing import Any


async def init(client: Any) -> None:
    plugin_dir = os.path.dirname(__file__)

    plugin_files = [
        f
        for f in os.listdir(plugin_dir)
        if f[0].isalpha()
        and f.endswith(".py")
        and f not in ("__init__.py", "__main__.py")
    ]

    plugin_files.sort(key=str.lower)

    plugins: list[ModuleType] = []
    for file in plugin_files:
        try:
            module = importlib.import_module(f"{__name__}.{file[:-3]}")
            plugins.append(module)
        except Exception:
            logging.exception(f"Failed to import plugin module {file}")

    plugins.sort(key=lambda m: (_get_priority(m), m.__name__.lower()))

    logging.debug("Plugin load order (priority: name):")
    for p in plugins:
        prio = _get_priority(p)
        logging.debug(f"  [{prio:3d}] {p.__name__.split('.')[-1]}")

    modules: dict[str, ModuleType] = {
        m.__name__.split(".")[-1]: m for m in plugins
    }

    for plugin in plugins:
        coro = _get_init_coro(plugin, client=client, modules=modules)
        if coro:
            await coro


def _get_priority(module: ModuleType) -> int:
    priority = getattr(
        module,
        "load_priority",
        1000,
    )
    if not isinstance(priority, int):
        logging.warning(
            "Plugin %s has invalid load_priority type (%s), using default 1000",
            module.__name__,
            type(priority).__name__,
        )
        return 1000
    return priority


def _get_init_coro(
    plugin: ModuleType,
    **kwargs: Any,
) -> Coroutine[Any, Any, None] | None:
    p_init = getattr(plugin, "init", None)
    if not callable(p_init):
        return None

    result_kwargs: dict[str, Any] = {}
    sig = inspect.signature(p_init)
    for param in sig.parameters.values():
        param_name = param.name
        if param_name in kwargs:
            result_kwargs[param_name] = kwargs[param_name]
        else:
            logging.error(
                "Handler plugin %s has unknown init parameter %s",
                plugin.__name__,
                param_name,
            )
            return None

    return _init_plugin(plugin, result_kwargs)


async def _init_plugin(plugin: ModuleType, kwargs: dict[str, Any]) -> None:
    try:
        logging.info(f"Loading handler plugin {plugin.__name__}…")
        start = time.time()
        ret = await plugin.init(**kwargs)
        took = time.time() - start
        logging.info(
            f"Loaded handler plugin {plugin.__name__} (took {took:.2f}s)",
        )
    except Exception:
        logging.exception(f"Failed to load handler plugin {plugin}")
    else:
        # Plugins may return a coroutine that should not just be lost.
        if asyncio.iscoroutine(ret):
            await ret


async def start_plugins(client: Any, plugins: list[ModuleType]) -> None:
    await asyncio.gather(
        *(_init_plugin(plugin, {"client": client}) for plugin in plugins),
    )
