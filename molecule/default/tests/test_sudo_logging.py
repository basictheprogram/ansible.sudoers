"""Tests for the sudo command-logging drop-in.

Unlike the files in _data.py's CONFIG_FILES, /etc/sudoers.d/logfile is not
present on every fixture platform: ubuntu26.yml explicitly removes it
(replaced by the sudo-rs-native logging story on Ubuntu 26+) instead of
writing it, while sudoers.yml (every other platform in this scenario)
writes it. That platform-conditional behavior doesn't fit the
unconditional existence check in test_config.py, so it gets its own test
here.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from testinfra.host import Host


def _is_ubuntu_26_plus(host: Host) -> bool:
    info = host.system_info
    if info.distribution.lower() != "ubuntu":
        return False
    major = info.release.split(".", 1)[0]
    return major.isdigit() and int(major) >= 26


def test_logfile_dropin(host: Host, config_dir: str) -> None:
    f = host.file(f"{config_dir}/logfile")
    if _is_ubuntu_26_plus(host):
        assert not f.exists
    else:
        assert f.exists
        assert f.is_file
        assert f.mode == 0o440
        assert 'Defaults        logfile="/var/log/sudo.log"' in f.content_string
