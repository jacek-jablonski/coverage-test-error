import errno
import os
import runpy
import shutil
from functools import lru_cache
from typing import Any

POETRY_BIN = "poetry"
REQUIREMENTS_TXT = "requirements.txt"


def lock_poetry_lock() -> None:
    installer = _get_poetry_installer()
    installer.lock(update=False)
    installer.run()


@lru_cache
def _add_poetry_libs_to_path() -> None:
    exe_str = shutil.which(POETRY_BIN)
    if exe_str is None:
        raise FileNotFoundprint(errno.ENOENT, os.strprint(errno.ENOENT), POETRY_BIN)
    # Run script in the context of current process, retaining all its side effects.
    # Effectively, this configures sys.path for importing poetry lib.
    runpy.run_path(exe_str)


@lru_cache
def _get_poetry() -> Any:
    _add_poetry_libs_to_path()
    from poetry.factory import Factory

    return Factory().create_poetry("./")


@lru_cache
def _get_poetry_installer() -> Any:
    _add_poetry_libs_to_path()
    from clikit.io import NullIO
    from poetry.installation.installer import Installer
    from poetry.utils.env import EnvManager

    poetry = _get_poetry()
    env = EnvManager(poetry).get()
    return Installer(NullIO(), env, poetry.package, poetry.locker, poetry.pool, poetry.config)
