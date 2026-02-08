import pytest
from testinfra.host import Host


@pytest.mark.parametrize(
    ("name", "version"),
    [
        ("nginx", "1.6"),
    ],
)
def test_packages(host: Host, name: str, version: str) -> None:
    pkg = host.package(name)
    assert pkg.is_installed
    assert pkg.version.startswith(version)
