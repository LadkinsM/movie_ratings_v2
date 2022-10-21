"""CRUD operations."""

from model import db, User, Movie, Rating, connect_to_db

#FUNCTIONS

def create_user(email, password):
    """Create and return a new user."""

    return User(email=email, password=password)

def create_movie(title, overview, release_date, poster_path):
    """Create and return a new movie."""

    return Movie(
        title=title, 
        overview=overview, 
        release_date=release_date, 
        poster_path=poster_path
    )

def create_rating(user, movie, score):
    """Create a rating"""

    return Rating(user=user, movie=movie, score=score)

if __name__ == '__main__':
    from server import app
    connect_to_db(app)