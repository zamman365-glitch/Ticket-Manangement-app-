import json
from pathlib import Path
class MovieBooking:
    database="Movies.json"
    data=[]
    if Path(database).exists():
        with open(database) as Myfile:
            data=json.load(Myfile)
    @classmethod
    def __update(cls):
        with open(cls.database,"w") as Myfile:
            Myfile.write(json.dumps(cls.data))
    def add_movie(self):
        movie={"movie_name" : input("enter the movie name"),
               "available_seats" :int(input("seats :"))}
        
        MovieBooking.data.append(movie)
        MovieBooking.__update()
        print("Movie added successfully.")
        
    def book_ticket(self):
        movie_name=input("Enter the movie name")
        movie=[i for i in MovieBooking.data if movie["movie_name"]==movie_name]
        if not movie:
            print("Movie not found.")
        return

        seats = int(input("How many seats do you want to book? "))

        if seats <= movie[0]["available_seats"]:
            movie[0]["available_seats"] -= seats
            MovieBooking.__update()
            print("Ticket booked successfully.")
        else:
            print("Not enough seats available.")

    def ticket_cancel(self):
            movie_name = input("Enter the movie name: ")
            movie = [ i for i in MovieBooking.data if i["movie_name"].lower() == movie_name.lower()]
            if not movie:
                print("Movie not found.")
            return 
            seats = int(input("How many tickets cancel? "))
            movie[0]["available_seats"] += seats
            MovieBooking.__update() 
            print("Ticket cancelled successfully")
    def show_movies(self):
        for movie in MovieBooking.data:
            print("\nMovie:", movie["movie_name"])
            print("Available Seats:", movie["available_seats"])

booking = MovieBooking()

print("1. Add Movie")
print("2. Book Ticket")
print("3. Cancel Ticket")
print("4. Show Movies")

choice = int(input("Enter your choice: "))

if choice == 1:
    booking.add_movie()

elif choice == 2:
    booking.book_ticket()

elif choice == 3:
    booking.cancel_ticket()

elif choice == 4:
    booking.show_movies()
    

