from movies import show_movies
from bookings import book_ticket

while True:

    print("\n🎬 MOVIE BOOKING SYSTEM")
    print("1. Show Movies")
    print("2. Book Ticket")
    print("3. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        show_movies()

    elif choice == "2":
        user_id = int(input("Enter User ID: "))
        movie_id = int(input("Enter Movie ID: "))
        seats = int(input("Enter Seats: "))

        book_ticket(user_id, movie_id, seats)

    elif choice == "3":
        print("👋 Goodbye!")
        break

    else:
        print("❌ Invalid choice")