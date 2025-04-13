from functools import lru_cache

import niquests  # pyright: ignore


@lru_cache
def pypi_package_exists(package: str) -> bool:  # pragma: no cover
    """Check if a package name exists on PyPI."""
    return (
        niquests.get(
            f'https://pypi.org/simple/{package}',
            timeout=15,
        ).status_code
        == 200
    )
