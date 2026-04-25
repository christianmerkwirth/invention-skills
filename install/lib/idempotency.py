"""Idempotency primitives for the installer.

Provides sha256 content comparison so that install scripts can skip
writing a file whose on-disk content already matches what would be
written.  This avoids mtime churn and false-positive diffs after
``git pull`` or ``git checkout`` (FR-05).
"""

from __future__ import annotations

import hashlib
from pathlib import Path


def content_hash(data: bytes | str) -> str:
    """Return the sha256 hex digest of *data*.

    If *data* is a ``str`` it is encoded as UTF-8 before hashing.
    """
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def file_matches(path: Path, expected_content: bytes | str) -> bool:
    """Return ``True`` iff *path* exists and its sha256 matches *expected_content*.

    Returns ``False`` if *path* does not exist or cannot be read.
    """
    try:
        on_disk = path.read_bytes()
    except (OSError, FileNotFoundError):
        return False

    return content_hash(on_disk) == content_hash(expected_content)
