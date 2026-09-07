import pathlib
from collections.abc import Iterator
from importlib.resources import as_file, files

import deadwood.adapters.db.alembic


def get_alembic_config_path() -> Iterator[pathlib.Path]:
    source = files(deadwood.adapters.db.alembic).joinpath("alembic.ini")
    with as_file(source) as path:
        yield path
