import pathlib
import uuid

import pytest
import pytest_asyncio
from alembic.config import Config
from yarl import URL

from deadwood.adapters.db.alembic.config import get_alembic_config_path
from deadwood.core import settings
from tests.utils.sqlachemy_utils import (
    create_database,
    database_exists,
    drop_database,
)


@pytest_asyncio.fixture(scope="session")
async def db_url():

    original_dsn = settings.get("db.database_url")

    url = URL(original_dsn)
    is_sqlite = "sqlite" in url.scheme

    if is_sqlite:
        original_path = pathlib.Path(
            url.path[1:] if url.path.startswith("/") else url.path,
        )
        test_db_path = original_path.with_name(
            f"{original_path.stem}.pytest.{uuid.uuid4().hex}{original_path.suffix}",
        )
        test_dsn = f"{url.scheme}:///{test_db_path.as_posix()}"
    else:
        tmp_name = f"{uuid.uuid4().hex}_pytest"
        test_dsn = str(url.with_path(tmp_name))
        if not await database_exists(test_dsn):
            await create_database(test_dsn)

    try:
        yield test_dsn
    finally:
        await drop_database(test_dsn)


@pytest.fixture(scope="session")
def alembic_config(db_url):
    alembic_path_gen = get_alembic_config_path()
    alembic_path = next(alembic_path_gen)
    alembic_cfg = Config(str(alembic_path))
    alembic_cfg.set_main_option(
        "script_location",
        str(alembic_path.parent / "migrations"),
    )
    alembic_cfg.set_main_option("sqlalchemy.url", db_url)
    return alembic_cfg
