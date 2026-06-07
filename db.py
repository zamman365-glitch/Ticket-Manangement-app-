"""
db.py — Database abstraction layer.
Centralises all connection management and raw query helpers.
Never import mysql.connector outside this module.
"""

from __future__ import annotations

import contextlib
from typing import Any, Generator

import mysql.connector
from mysql.connector import pooling

# ---------------------------------------------------------------------------
# Configuration — swap these for env-vars / Secrets in production
# ---------------------------------------------------------------------------
_DB_CONFIG: dict[str, Any] = {
    "host": "localhost",
    "user": "root",
    "password": "root123",
    "database": "movie_booking",
}

_POOL_NAME = "movie_pool"
_POOL_SIZE = 5

# Build a connection pool once at module import time.
# Falls back to a plain connect() if the pool cannot be created
# (e.g. during local dev without a running DB).
try:
    _pool = pooling.MySQLConnectionPool(
        pool_name=_POOL_NAME,
        pool_size=_POOL_SIZE,
        **_DB_CONFIG,
    )
except Exception:
    _pool = None  # type: ignore[assignment]


def get_connection() -> mysql.connector.MySQLConnection:
    """Return a live connection, from the pool when available."""
    if _pool:
        return _pool.get_connection()
    return mysql.connector.connect(**_DB_CONFIG)


@contextlib.contextmanager
def db_cursor(
    commit: bool = False,
    dictionary: bool = True,
) -> Generator[mysql.connector.cursor.MySQLCursor, None, None]:
    """
    Context-manager that yields a cursor and handles connection lifecycle.

    Usage::

        with db_cursor(commit=True) as cur:
            cur.execute("INSERT INTO ...")

    Args:
        commit:     Auto-commit the transaction on successful exit.
        dictionary: Return rows as dicts (True) or tuples (False).
    """
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=dictionary)
        yield cursor
        if commit:
            conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()
