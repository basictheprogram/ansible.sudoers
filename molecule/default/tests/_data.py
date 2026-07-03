"""Shared test constants for the sudoers Molecule scenario."""

from __future__ import annotations

# 1. OS-family detection.
REDHAT_DISTROS: frozenset[str] = frozenset({"redhat", "centos", "rocky", "almalinux", "fedora"})

# 2. Packages this role should install, per OS family.
# From vars/Debian.yml / defaults/main.yml -- RedHat/EL currently gets no
# packages installed by this role (no vars/RedHat.yml exists; it falls back
# to defaults/main.yml's empty sudoers_packages: []).
DEBIAN_PACKAGES: list[str] = ["sudo", "lsb-release"]
REDHAT_PACKAGES: list[str] = []

# 3. Config directory this role writes into. Fixed across every supported OS
# family -- always /etc/sudoers.d -- so there is no per-family variant to
# track here (see conftest.py's config_dir fixture).
SUDOERS_D: str = "/etc/sudoers.d"

# 4. Config files this role renders on every fixture platform, for
# existence/permission checks. testuser1/testuser2 come from the
# community.general.sudoers module (one file per management_user entry,
# named after item.username by default); ssh_auth_sock and veeam12 are
# fixed filenames written by sudoers.yml/ubuntu26.yml. "logfile" is
# deliberately excluded here -- it exists on every fixture platform except
# ubuntu-resolute (Ubuntu 26+ removes it instead of writing it), so it gets
# its own conditional test in test_sudo_logging.py rather than the
# unconditional CONFIG_FILES existence check.
CONFIG_FILES: list[str] = [
    "ssh_auth_sock",
    "veeam12",
    "testuser1",
    "testuser2",
]
