# from db import get_connection

# def book_ticket(user_id, movie_id, seats):
#     conn = get_connection()
#     cursor = conn.cursor()

#     cursor.execute("SELECT available_seats FROM movies WHERE movie_id=%s", (movie_id,))
#     result = cursor.fetchone()

#     if result and result[0] >= seats:

#         cursor.execute(
#             "INSERT INTO bookings (user_id, movie_id, seats_booked) VALUES (%s, %s, %s)",
#             (user_id, movie_id, seats)
#         )

#         cursor.execute(
#             "UPDATE movies SET available_seats = available_seats - %s WHERE movie_id=%s",
#             (seats, movie_id)
#         )

#         conn.commit()
#         print("🎟 Booking Successful!")

#     else:
#         print("❌ Not enough seats")

#     conn.close()


"""
bookings.py — Bookings repository.
Handles transactional seat reservation with optimistic-lock style checks.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from db import db_cursor


@dataclass
class BookingResult:
    success: bool
    message: str
    booking_id: int | None = None


def book_ticket(user_id: int, movie_id: int, seats: int) -> BookingResult:
    """
    Reserve `seats` for `user_id` on `movie_id`.

    Runs inside a single transaction:
      1. Re-reads available_seats (prevents TOCTOU race condition).
      2. Inserts the booking row.
      3. Decrements available_seats atomically.

    Returns a BookingResult so the caller never catches raw DB exceptions.
    """
    if seats < 1:
        return BookingResult(success=False, message="Please select at least 1 seat.")

    try:
        with db_cursor(commit=True) as cur:
            # Step 1 — lock row for the duration of this transaction
            cur.execute(
                "SELECT available_seats FROM movies WHERE movie_id = %s FOR UPDATE",
                (movie_id,),
            )
            row = cur.fetchone()

            if not row:
                return BookingResult(success=False, message="Movie not found.")

            if row["available_seats"] < seats:
                return BookingResult(
                    success=False,
                    message=f"Only {row['available_seats']} seat(s) left.",
                )

            # Step 2 — create the booking
            cur.execute(
                """
                INSERT INTO bookings (user_id, movie_id, seats_booked, booking_time)
                VALUES (%s, %s, %s, NOW())
                """,
                (user_id, movie_id, seats),
            )
            booking_id = cur.lastrowid

            # Step 3 — decrement seats atomically
            cur.execute(
                """
                UPDATE movies
                SET available_seats = available_seats - %s
                WHERE movie_id = %s
                """,
                (seats, movie_id),
            )

        return BookingResult(
            success=True,
            message=f"Booking confirmed! 🎟 {seats} seat(s) reserved.",
            booking_id=booking_id,
        )

    except Exception as exc:  # noqa: BLE001
        return BookingResult(success=False, message=f"Database error: {exc}")


def get_bookings_by_user(user_id: int) -> list[dict[str, Any]]:
    """Fetch all bookings for a given user, joined with movie title."""
    with db_cursor() as cur:
        cur.execute(
            """
            SELECT
                b.booking_id,
                b.seats_booked,
                b.booking_time,
                m.title,
                m.genre,
                m.language,
                m.ticket_price,
                (b.seats_booked * m.ticket_price) AS total_amount
            FROM bookings b
            JOIN movies m ON b.movie_id = m.movie_id
            WHERE b.user_id = %s
            ORDER BY b.booking_time DESC
            """,
            (user_id,),
        )
        return cur.fetchall()


def cancel_booking(booking_id: int, user_id: int) -> BookingResult:
    """Cancel a booking and restore seats."""
    try:
        with db_cursor(commit=True) as cur:
            cur.execute(
                "SELECT * FROM bookings WHERE booking_id = %s AND user_id = %s",
                (booking_id, user_id),
            )
            booking = cur.fetchone()
            if not booking:
                return BookingResult(success=False, message="Booking not found.")

            cur.execute(
                "DELETE FROM bookings WHERE booking_id = %s",
                (booking_id,),
            )
            cur.execute(
                """
                UPDATE movies
                SET available_seats = available_seats + %s
                WHERE movie_id = %s
                """,
                (booking["seats_booked"], booking["movie_id"]),
            )

        return BookingResult(
            success=True,
            message="Booking cancelled and seats restored.",
            booking_id=booking_id,
        )
    except Exception as exc:  # noqa: BLE001
        return BookingResult(success=False, message=f"Database error: {exc}")
