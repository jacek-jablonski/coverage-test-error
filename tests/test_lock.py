import os
import shutil
from pathlib import Path

from pytest import fixture
from pytest_mock import MockerFixture

from poetry_tools import lock


def test_poetry_lock_locking(tmp_path: Path, mocked_locks_path: Path, mocker: MockerFixture) -> None:
    shutil.copy(mocked_locks_path / "pyproject.toml", tmp_path / "pyproject.toml")
    os.chdir(tmp_path)
    lock._add_poetry_libs_to_path()
    installer_mock = mocker.patch("poetry.installation.installer.Installer")
    lock.lock_poetry_lock()

    installer_mock.return_value.lock.assert_called_once_with(update=False)
    installer_mock.return_value.run.assert_called_once()


@fixture(scope="session")
def mocked_locks_path() -> Path:
    return (Path(__file__) / "../locks").resolve()


@fixture(autouse=True)
def mock_lru_cache() -> None:
    lock._add_poetry_libs_to_path.cache_clear()
    lock._get_poetry.cache_clear()
    lock._get_poetry_installer.cache_clear()
