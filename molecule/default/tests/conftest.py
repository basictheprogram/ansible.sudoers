"""Session-scoped pytest fixtures for the sudoers Molecule scenario."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from ._data import SUDOERS_D

if TYPE_CHECKING:
    from testinfra.host import Host


@pytest.fixture(scope="module")
def config_dir(host: Host) -> str:
    # Fixed path across every OS family this role supports -- unlike most
    # roles that use this fixture pattern, there is no per-family branch
    # here (see _data.py's SUDOERS_D comment).
    del host
    return SUDOERS_D
