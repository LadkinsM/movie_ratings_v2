"""
Seed the Database
Automatically:

dropdb
createdb
db.create_all
populate database with movie, user, and ratings data
"""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system("dropdb ratings")
os.system('createdb ratings')

model.connect_to_db(server.app)
model.db.create_all()

#Load movie data from JSON file
with open('data/movies.json') as f:
    movie_data = json.loads(f.read())

# Create movies, store them in list so we can use them
# to create fake ratings later
movies_in_db = []

for movie in movie_data:
    # TODO: get the title, overview, and poster_path from the movie
    # dictionary. Then, get the release_date and convert it to a
    # datetime object with datetime.strptime

    title, overview, poster_path = (movie['title'], movie['overview'], movie['poster_path'])

    release_date_data = movie['release_date']
    format = "%Y-%m-%d"
    release_date = datetime.strptime(release_date_data, format)

    # TODO: create a movie here and append it to movies_in_db
    movies_in_db.append(crud.create_movie(title, overview, release_date, poster_path))

model.db.session.add_all(movies_in_db)
model.db.session.commit()

for n in range(10):
    email = f'user{n}@test.com'  # Voila! A unique email!
    password = 'test'

    # TODO: create a user here
    user = crud.create_user(email, password)
    model.db.session.add(user)

    # TODO: create 10 ratings for the user
    for i in range(10):
        rating = crud.create_rating(user, choice(movies_in_db), randint(1,5))
        model.db.session.add(rating)

model.db.session.commit()