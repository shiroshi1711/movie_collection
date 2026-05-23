from datetime import datetime as dt
from pathlib import Path
import re
import json
import csv
import requests

class InvalidMovieRatingError(Exception):
    pass

class DuplicateMovieError(Exception):
    pass

class Movie:
    def __init__(self, title, year, genre, rating):
        self.title = title
        self.year = int(year)
        self.genre = genre
        self.set_rating(rating)

    def get_rating(self):
        return self.__rating
    
    def set_rating(self, value):
        value = float(value)
        if value < 0 or value > 10:
            raise InvalidMovieRatingError ("Invalid Rating!")
        self.__rating = value

    def introduce(self):
        print(f"🎬 {self.title} ({self.year}) - {self.genre} - ⭐{self.get_rating()}/10!")

    def to_dict(self):
        data = {
            "title" : self.title,
            "year" : str(self.year),
            "genre" : self.genre,
            "rating" : str(self.get_rating())
        }
        return data

class MovieCollection:
    def __init__(self, filename):
        self.filename = filename
        self.movie_list = []

    def log_action(func):
        def wrapper (self, *args, **kwargs):
            print("Action started....")
            print()
            func(self,*args, **kwargs)
            print()
            print("Action ended.")
        return wrapper
    
    @log_action
    def add_movie(self, data):
        for movie in self.movie_list:
            if data.title == movie.title :
                raise DuplicateMovieError ("Movie already exist!")
        self.movie_list.append(data)
        print(f"Added {data.title} to the list!")

    @log_action
    def show_all(self):
        print("{:^80}".format("Movie list"))
        print("=" * 80)
        print("{:<3}{:^37}{:<10}{:^20}{:>10}".format("No", "Title", "Year", "Genre", "Rating"))
        print("=" * 80)
        for i, movie in enumerate(self.movie_list, 1):
            print(f"{i:<3}{movie.title:<37}{movie.year:<10}{movie.genre:^20}{movie.get_rating():>7}/10")

    def get_best_movie(self):
        print("{:^80}".format("Best Movie list"))
        print("=" * 80)
        print("{:<3}{:^37}{:<10}{:^20}{:>10}".format("No", "Title", "Year", "Genre", "Rating"))
        print("=" * 80)
        for i, movie in enumerate(self.movie_list, 1):
            if movie.get_rating() >= 8:
                print(f"{i:<3}{movie.title:<37}{movie.year:<10}{movie.genre:^20}{movie.get_rating():>7}/10")

    def filter_by_genre(self, g):
        print("{:^60}".format(f"Movie in genre {g}"))
        print("=" * 60)
        print("{:<3}{:^37}{:<10}{:>10}".format("No", "Title", "Year", "Rating"))
        print("=" * 60)
        found = False
        for i, movie in enumerate(self.movie_list, 1):
            if g == movie.genre:
                print(f"{i:<3}{movie.title:<37}{movie.year:<10}{movie.get_rating():>7}/10")
                found = True
        if not found:
            print(f"No movie in {g} genre!")

    def export_to_csv(self):
        file = Path("moviecollection.csv")
        try:
            with file.open("w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "Title",
                    "Year",
                    "Genre",
                    "Rating"
                ])

                for movie in self.movie_list:
                    writer.writerow([
                        movie.title,
                        movie.year,
                        movie.genre,
                        movie.get_rating()
                    ])
            print("Success!")
        except Exception as e:
            print(e)

    def load_from_json(self):
        self.movie_list.clear()
        file = Path(self.filename)
        try:
            if file.exists():
                loaded_file = json.loads(file.read_text())
                for movie in loaded_file:
                    movie_object = Movie(movie["title"], movie["year"], movie["genre"], movie["rating"])
                    self.movie_list.append(movie_object)
            else:
                print("Movie list is empty!")
        except Exception as e:
            print(e)

    def save_to_json(self):
        dictdata = []
        try:
            for movie in self.movie_list:
                movie_dict = movie.to_dict()
                dictdata.append(movie_dict)
            file = Path(self.filename)
            file.write_text(json.dumps(dictdata, indent=4))
            print("Saved to JSON!") 
        except Exception as e:
            print(e)

    
json_filename = "moviecollection.json"
manager = MovieCollection(json_filename)

manager.load_from_json()

movie1 = Movie("Spirited Away", 2001, "Fantasy", 8.9)
movie2 = Movie("Your Name", 2016, "Romance", 8.4)
movie3 = Movie("Howl's Moving Castle", 2004, "Fantasy", 8.2)
movie4 = Movie("A Silent Voice", 2016, "Drama", 8.9)
movie5 = Movie("Princess Mononoke", 1997, "Adventure", 8.7)
movie6 = Movie("Weathering With You", 2019, "Romance", 7.9)
movie7 = Movie("Suzume", 2022, "Fantasy", 7.8)
movie8 = Movie("Perfect Blue", 1997, "Psychological", 8.0)
movie9 = Movie("Akira", 1988, "Sci-Fi", 8.0)
movie10 = Movie("The Boy and the Heron", 2023, "Fantasy", 7.6)
movie11 = Movie("Interstellar", 2014, "Sci-Fi", 9.5)
movie12= Movie("The Dark Knight", 2008, "Action", 9.3)
movie13= Movie("Parasite", 2019, "Thriller", 8.6)
movie14 = Movie("Shrek", 2001, "Comedy", 8.1)
movie15= Movie("La La Land", 2016, "Musical", 8.0)
movie16= Movie("Avengers Endgame", 2019, "Superhero", 8.4)
movie17= Movie("The Godfather", 1972, "Crime", 9.2)
movie18 = Movie("Inception", 2010, "Sci-Fi", 8.8)

m_list = [movie1, movie2, movie3, movie4, movie5, movie6, movie7, movie8, movie9,
          movie10, movie11, movie12, movie13, movie14, movie15, movie16, movie17, movie18]
for m in m_list:
    try:
        manager.add_movie(m)
    except DuplicateMovieError as e:
        print(e)

manager.show_all()

manager.get_best_movie()

manager.filter_by_genre("Fantasy")

manager.export_to_csv()

manager.save_to_json()

print()

def top_rated_movies(movies,min_rating):
    for movie in movies:
        if movie.get_rating() >= min_rating:
            yield movie

top_movies = top_rated_movies(manager.movie_list, 9)

for m in top_movies:
    print(m.title)

print()
response = requests.get("https://jsonplaceholder.typicode.com/posts")

if response.status_code == 200:
    print("success!")
    data = response.json()
    for post in data[:3]:
        print(f"{post['title']}") 
else:
    (f"Error! : {response.status_code}")

print()
#get the rating
reviews = "Interstellar 9.5/10, The Dark Knight 9.8/10, Inception 9.2/10"

rating = re.findall(r"\d+\.\d+/\d+", reviews)
print(rating)