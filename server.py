"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify)
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """Homepage"""

    return render_template('homepage.html')

# MOVIE-RELATED

@app.route('/movies')
def all_movies():
    """View all movies."""

    movies = crud.get_movies()

    return render_template('all_movies.html', movies=movies)

@app.route('/movies/<movie_id>')
def selected_movie(movie_id):
    """Displays movie details"""
    
    movie = crud.get_movie_by_id(movie_id)

    return render_template('movie_details.html', movie=movie)

# USER-RELATED

@app.route('/users')
def all_users():
    """""View all users."""
    
    users = crud.get_users()

    return render_template('all_users.html', users=users)

@app.route('/users', methods=['POST'])
def register_user():
    """"Create new user."""

    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)

    if user:
        flash('That email is already being used, please try again with a different email.')
    else:
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, your account has been created and you can now login!')
        
    return redirect('/')

@app.route('/login', methods=['POST'])
def check_user():
    """Login existing user."""

    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)

    if user:
        if user.password == password:
            session['user'] = user.user_id
            flash('Logged In!')
        else:
            flash('Your password is incorrect.')
    else:
        flash('Your username is incorrect. Please input a valid username & password.')
    
    return redirect('/')

@app.route('/users/<user_id>')
def selected_user(user_id):
    """Displays user details"""

    user = crud.get_user_by_id(user_id)

    return render_template('user_details.html', user=user)

#RATINGS

@app.route('/movies/<movie_id>/rating', methods= ['POST'])
def add_rating(movie_id):
    """Adds user rating"""

    user_id = int(session['user'])
    movie_id = int(movie_id)
    score = request.form.get('score', type=int)

    rating = crud.create_rating(user_id, movie_id, score)

    db.session.add(rating)
    db.session.commit()

    return render_template('movie_details.html', movie=crud.get_movie_by_id(movie_id))

@app.route('/movies/<movie_id>/ratings')
def return_rating(movie_id):
    user_id = int(session['user'])
    movie_id = int(movie_id)

    rating = crud.get_rating_by_movie_id(movie_id, user_id)

    if 'user' in session:
        return jsonify({"user_id":rating.user_id,
                        "score":rating.score})
    
    return jsonify({"score": "You must be logged in to view your rating."})
    

    

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
