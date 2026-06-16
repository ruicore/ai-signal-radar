from __future__ import annotations

from scripts.validate_content import validate


def test_repository_content_is_valid() -> None:
    assert validate() == []
