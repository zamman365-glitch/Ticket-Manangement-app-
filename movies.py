from db import get_connection

def show_movies():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM movies")
    for row in cursor.fetchall():
        print(row)

    conn.close()