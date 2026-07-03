"""Config-file tests for the sudoers Molecule scenario.

Parametrized existence/permission checks over CONFIG_FILES. Content
assertions get their own single-purpose test function per file/setting
pair -- never combine an existence check and a content check in the same
test function.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from ._data import CONFIG_FILES

if TYPE_CHECKING:
    from testinfra.host import Host


@pytest.mark.parametrize("filename", CONFIG_FILES)
def test_config_file_exists(host: Host, config_dir: str, filename: str) -> None:
    f = host.file(f"{config_dir}/{filename}")
    assert f.exists
    assert f.is_file


@pytest.mark.parametrize("filename", CONFIG_FILES)
def test_config_file_mode(host: Host, config_dir: str, filename: str) -> None:
    f = host.file(f"{config_dir}/{filename}")
    assert f.mode == 0o440


@pytest.mark.parametrize("filename", CONFIG_FILES)
def test_config_file_owned_by_root(host: Host, config_dir: str, filename: str) -> None:
    f = host.file(f"{config_dir}/{filename}")
    assert f.user == "root"


def test_ssh_auth_sock_content(host: Host, config_dir: str) -> None:
    f = host.file(f"{config_dir}/ssh_auth_sock")
    assert 'Defaults    env_keep += "SSH_AUTH_SOCK"' in f.content_string


def test_veeam12_content(host: Host, config_dir: str) -> None:
    f = host.file(f"{config_dir}/veeam12")
    assert "Cmnd_Alias VEEAM12_COMMANDS" in f.content_string
    assert "veeam12 ALL=(root) NOPASSWD: VEEAM12_COMMANDS" in f.content_string


@pytest.mark.parametrize("username", ["testuser1", "testuser2"])
def test_management_user_nopasswd(host: Host, config_dir: str, username: str) -> None:
    # community.general.sudoers formats the generated line itself, so this
    # checks the substrings that must be present rather than an exact
    # literal line (whitespace is module-controlled, not role-controlled).
    f = host.file(f"{config_dir}/{username}")
    assert username in f.content_string
    assert "NOPASSWD" in f.content_string
    assert "ALL" in f.content_string
