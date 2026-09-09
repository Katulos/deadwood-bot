import pytest
from alembic.command import downgrade, upgrade
from alembic.config import Config
from alembic.script import Script, ScriptDirectory

from deadwood.adapters.db.alembic.config import get_alembic_config_path


def get_revisions():
    alembic_path_gen = get_alembic_config_path()
    alembic_path = next(alembic_path_gen)
    revisions_dir = ScriptDirectory(str(alembic_path.parent / "migrations"))

    revisions = list(revisions_dir.walk_revisions("base", "heads"))
    revisions.reverse()
    return revisions


@pytest.mark.order(1)
@pytest.mark.parametrize("revision", get_revisions())
def test_migrations_stairway(revision: Script, alembic_config: Config):
    upgrade(alembic_config, revision.revision)

    downgrade(alembic_config, revision.down_revision or "-1")

    upgrade(alembic_config, revision.revision)
