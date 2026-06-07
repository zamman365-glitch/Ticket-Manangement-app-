# # from db import get_connection

# # def show_movies():
# #     conn = get_connection()
# #     cursor = conn.cursor()

# #     cursor.execute("SELECT * FROM movies")
# #     for row in cursor.fetchall():
# #         print(row)

# #     conn.close()

# """
# movies.py — Movies repository.
# All queries related to the `movies` table live here.
# """

# from __future__ import annotations

# from typing import Any

# from db import db_cursor


# def get_all_movies():
#     with db_cursor() as cur:
#         cur.execute("SELECT * FROM movies")
#         rows = cur.fetchall()
#         return rows


# def get_movie_by_id(movie_id: int) -> dict[str, Any] | None:
#     """Return a single movie row or None."""
#     with db_cursor() as cur:
#         cur.execute(
#             "SELECT * FROM movies WHERE movie_id = %s",
#             (movie_id,),
#         )
#         return cur.fetchone()


# def get_available_seats(movie_id: int) -> int:
#     """Return the current seat count for a movie."""
#     with db_cursor() as cur:
#         cur.execute(
#             "SELECT available_seats FROM movies WHERE movie_id = %s",
#             (movie_id,),
#         )
#         row = cur.fetchone()
#         return row["available_seats"] if row else 0


# def search_movies(query: str) -> list[dict[str, Any]]:
#     """Full-text style search across title, genre, and language."""
#     like = f"%{query}%"
#     with db_cursor() as cur:
#         cur.execute(
#             """
#             SELECT * FROM movies
#             WHERE title LIKE %s OR genre LIKE %s OR language LIKE %s
#             ORDER BY release_date DESC
#             """,
#             (like, like, like),
#         )
#         return cur.fetchall()

# from db import db_cursor


# def get_all_movies():
#     with db_cursor() as cur:
#         cur.execute("SELECT * FROM movies")
#         rows = cur.fetchall()
#         return rows


# def search_movies(query: str):
#     like = f"%{query}%"
#     with db_cursor() as cur:
#         cur.execute("""
#             SELECT * FROM movies
#             WHERE movie_name LIKE %s
#         """, (like,))
#         return cur.fetchall()


# def get_available_seats(movie_id: int):
#     with db_cursor() as cur:
#         cur.execute(
#             "SELECT available_seats FROM movies WHERE movie_id = %s",
#             (movie_id,)
#         )
#         row = cur.fetchone()
#         return row["available_seats"] if row else 0


# def get_movie_by_id(movie_id: int):
#     with db_cursor() as cur:
#         cur.execute(
#             "SELECT * FROM movies WHERE movie_id = %s",
#             (movie_id,)
#         )
#         return cur.fetchone()

from db import db_cursor


def get_all_movies():
    with db_cursor() as cur:
        cur.execute("SELECT * FROM movies")
        return cur.fetchall()


def search_movies(query: str):
    like = f"%{query}%"
    with db_cursor() as cur:
        cur.execute("""
            SELECT * FROM movies
            WHERE movie_name LIKE %s
        """, (like,))
        return cur.fetchall()


def get_movie_by_id(movie_id: int):
    with db_cursor() as cur:
        cur.execute(
            "SELECT * FROM movies WHERE movie_id = %s",
            (movie_id,)
        )
        return cur.fetchone()


def get_available_seats(movie_id: int):
    with db_cursor() as cur:
        cur.execute(
            "SELECT available_seats FROM movies WHERE movie_id = %s",
            (movie_id,)
        )
        row = cur.fetchone()
        return row["available_seats"] if row else 0