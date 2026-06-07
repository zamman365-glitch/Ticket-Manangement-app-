from db import get_connection

def book_ticket(user_id, movie_id, seats):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT available_seats FROM movies WHERE movie_id=%s", (movie_id,))
    result = cursor.fetchone()

    if result and result[0] >= seats:

        cursor.execute(
            "INSERT INTO bookings (user_id, movie_id, seats_booked) VALUES (%s, %s, %s)",
            (user_id, movie_id, seats)
        )

        cursor.execute(
            "UPDATE movies SET available_seats = available_seats - %s WHERE movie_id=%s",
            (seats, movie_id)
        )

        conn.commit()
        print("🎟 Booking Successful!")

    else:
        print("❌ Not enough seats")

    conn.close()