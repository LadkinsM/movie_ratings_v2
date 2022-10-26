"""CRUD operations."""

from model import db, User, Movie, Rating, connect_to_db

#FUNCTIONS

#USER-RELATED

def create_user(email, password):
    """Create and return a new user."""

    return User(email=email, password=password)

def get_users():
    """Returns all users"""

    return User.query.all()
    
def get_user_by_id(user_id):
    """Return user info by id"""

    return User.query.get(user_id)

def get_user_by_email(email):
    """Return a user with inputted email"""

    return User.query.filter(User.email == email).first()

#MOVIE-RELATED

def create_movie(title, overview, release_date, poster_path):
    """Create and return a new movie."""

    return Movie(
        title=title, 
        overview=overview, 
        release_date=release_date, 
        poster_path=poster_path
    )

def get_movies():
    """Returns all movies"""

    return Movie.query.all()

def get_movie_by_id(movie_id):
    """Return movie info by id"""

    return Movie.query.get(movie_id)

#RATING-RELATED

def create_rating(user_id, movie_id, score):
    """Create a rating"""

    return Rating(user_id=user_id, movie_id=movie_id, score=score)

def get_rating_by_movie_id(movie_id, user_id):
    """Return users rating"""

    return db.session.query(Rating.score).filter(Rating.movie_id==movie_id, Rating.user_id==user_id).first()

    # return Rating.query.filter(Rating.movie_id==movie_id).all()

if __name__ == '__main__':
    from server import app
    connect_to_db(app)