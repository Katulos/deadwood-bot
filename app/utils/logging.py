import logging
import sys
from typing import Any

import structlog

from .tools import orjson_dumps


class _StructlogFormatter(logging.Formatter):
    def __init__(self, processors: list[structlog.typing.Processor]):
        super().__init__()
        self._processors = processors
        self._global_context: dict[str, Any] = {}

    def update_global_context(self, new_values: dict[str, Any]) -> None:
        self._global_context.update(new_values)

    def format(self, record: logging.LogRecord) -> str:
        if record.args:
            record.msg = record.msg % record.args
            record.args = None

        record_dict: dict[str, Any] = {
            "event": record.msg,
            "level": record.levelno,
        }

        if record.name == "root":
            record_dict.update(self._global_context)

        if record.exc_info:
            record_dict["exc_info"] = record.exc_info

        for processor in self._processors:
            try:
                result = processor(
                    None,
                    record.levelname.lower(),
                    record_dict,
                )
                if isinstance(result, str):
                    return result
                elif isinstance(result, dict):
                    record_dict = result
            except Exception:
                continue

        if isinstance(record_dict, dict) and "event" in record_dict:
            return str(record_dict["event"])
        return str(record_dict)


def setup_logger(
    logging_level: int = logging.INFO,
) -> structlog.typing.FilteringBoundLogger:
    shared_processors: list[structlog.typing.Processor] = [
        structlog.processors.add_log_level,
    ]

    processors: list[structlog.typing.Processor] = [*shared_processors]

    if sys.stderr.isatty():
        processors.extend(
            [
                structlog.processors.TimeStamper(fmt="iso", utc=True),
                structlog.dev.ConsoleRenderer(),
            ],
        )
    else:
        processors.extend(
            [
                structlog.processors.TimeStamper(fmt=None, utc=True),
                structlog.processors.dict_tracebacks,
                structlog.processors.JSONRenderer(serializer=orjson_dumps),
            ],
        )

    formatter = _StructlogFormatter(processors)

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(logging_level),
        cache_logger_on_first_use=True,
    )

    root_logger = logging.getLogger()
    root_logger.handlers.clear()

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
    root_logger.setLevel(logging_level)

    logger = structlog.get_logger()

    original_bind = logger.bind

    def patched_bind(
        **new_values: Any,
    ) -> structlog.typing.FilteringBoundLogger:
        if logger is structlog.get_logger():
            formatter.update_global_context(new_values)
        return original_bind(**new_values)

    logger.bind = patched_bind

    return logger
