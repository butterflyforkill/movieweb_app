from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """
    Represents a user in the system.

    Attributes:
        id (int): The unique identifier for the user (primary key).
        user_name (str): The username of the user (not nullable).
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(100), nullable = False)


class Movie(db.Model):
    """
    Represents a movie in the system.

    Attributes:
        id (int): The unique identifier for the movie (primary key).
        movie_poster (str): URL or path to the movie poster (not nullable).
        movie_name (str): The title of the movie (not nullable, unique).
        movie_director (str): The director of the movie (not nullable).
        release_year (int): The year the movie was released (not nullable).
        movie_rating (float): The average rating of the movie (not nullable).
        movie_plot (str): A description of the movie plot (not nullable).
    """
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    movie_poster = db.Column(db.Text, nullable = False)
    movie_name = db.Column(db.String(250), nullable = False, unique=True)
    movie_director = db.Column(db.String(100), nullable = False)
    release_year = db.Column(db.Integer, nullable = False)
    movie_rating = db.Column(db.Float, nullable = False)
    movie_plot = db.Column(db.Text, nullable = False)


class UserMovie(db.Model):
    """
    Represents the association between a user and a movie in their list.

    Attributes:
        user_id (int): The foreign key referencing the User model (primary key).
        movie_id (int): The foreign key referencing the Movie model (primary key).
        watchlist_status (str, optional): The user's watchlist status for the movie (e.g., 'watched', 'watching', 'wishlist').
        user_rating (int, optional): The user's rating for the movie.
        user (User): Relationship with the User model.
        movie (Movie): Relationship with the Movie model.
    """
    __tablename__ = 'users_movies'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), primary_key=True)
    watchlist_status = db.Column(db.String(10), nullable = True)  # Example: 'watched', 'watching', 'wishlist'
    user_rating = db.Column(db.Integer, nullable = True)
    user = db.relationship('User', backref='user_movies')
    movie = db.relationship('Movie', backref='user_movies')
    
    def __str__(self):
        """
        Returns a human-readable representation of a UserMovie object.

        Includes user ID, movie ID, watchlist status (if set), and user rating (if set).
        """

        status_string = f" (watchlist status: {self.watchlist_status})" if self.watchlist_status else ""
        rating_string = f" (rating: {self.user_rating})" if self.user_rating else ""

        return f"UserMovie(user_id={self.user_id}, movie_id={self.movie_id}{status_string}{rating_string})"