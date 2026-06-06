import json
import pathlib as path 
class MovieBooking:
    database="Movies.json"
    data=[]
    if path(database).exists():
        with open(database) as Myfile:
            data=json.load(Myfile)
    @classmethod
    def __update(cls):
        with open(cls.database,"w") as Myfile:
            Myfile.write(json.dumps(cls.data))
    def addmovie(self):
        movie={"movie_name" : input("enter the movie name"),
               "available_seats" :int(input("seats :"))}

           