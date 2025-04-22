import structlog
import tenacity
import tortoise
from tenacity import _utils

TIMEOUT_BETWEEN_ATTEMPTS = 2
MAX_TIMEOUT = 30


def before_log(retry_state: tenacity.RetryCallState) -> None:
    if retry_state.outcome is None:
        return

    logger = retry_state.kwargs["logger"]
    if retry_state.outcome.failed:
        verb, value = "raised", retry_state.outcome.exception()
    else:
        verb, value = "returned", retry_state.outcome.result()

    callback_name = _utils.get_callback_name(retry_state.fn)
    sleep_time = retry_state.next_action.sleep

    logger.info(
        f"Retrying {callback_name} in {sleep_time} seconds as it {verb} {value}",
        extra={
            "callback": callback_name,
            "sleep": sleep_time,
            "verb": verb,
            "value": value,
        },
    )


def after_log(retry_state: tenacity.RetryCallState) -> None:
    logger = retry_state.kwargs["logger"]
    callback_name = _utils.get_callback_name(retry_state.fn)
    elapsed_time = retry_state.seconds_since_start
    attempt = _utils.to_ordinal(retry_state.attempt_number)

    logger.info(
        f"Finished call to {callback_name} after {elapsed_time:.2f} seconds, this was the {attempt} attempt",
        extra={
            "callback": callback_name,
            "time": elapsed_time,
            "attempt": attempt,
        },
    )


@tenacity.retry(
    wait=tenacity.wait_fixed(TIMEOUT_BETWEEN_ATTEMPTS),
    stop=tenacity.stop_after_delay(MAX_TIMEOUT),
    before_sleep=before_log,
    after=after_log,
)  # type: ignore
async def wait_db(
    *,
    logger: structlog.typing.FilteringBoundLogger,
    dsn: str,
) -> None:
    config = {
        "connections": {"default": dsn},
        "apps": {
            "app": {
                "models": ["app.database.models"],
                "default_connection": "default",
            },
        },
    }
    await tortoise.Tortoise.init(config=config)

    conn: tortoise.BaseDBAsyncClient = tortoise.connections.get("default")
    await conn.execute_script("SELECT 1")
    logger.debug("Successfully connected to database")

    await tortoise.Tortoise.generate_schemas()
    logger.debug("Database schemas generated successfully")


@tenacity.retry(
    wait=tenacity.wait_fixed(TIMEOUT_BETWEEN_ATTEMPTS),
    stop=tenacity.stop_after_delay(MAX_TIMEOUT),
    before_sleep=before_log,
    after=after_log,
)  # type: ignore
async def wait_close_db(
    *,
    logger: structlog.typing.FilteringBoundLogger,
) -> None:
    await tortoise.Tortoise.close_connections()
    logger.debug("Database connections closed successfully")
