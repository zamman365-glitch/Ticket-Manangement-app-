import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root123",
    database="movie_booking"
)

cursor = conn.cursor()

print("✅ Connected to MySQL Successfully!")

cursor.execute("SELECT * FROM movies")

movies = cursor.fetchall()

print("\n🎬 Available Movies:\n")
for m in movies:
    print(m)


def book_ticket(user_id, movie_id, seats):

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
        print("❌ Not enough seats available")

        
conn.commit()

book_ticket(1, 1, 2)