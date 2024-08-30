from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(100), nullable = False)


class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    movie_name = db.Column(db.String(250), nullable = False)
    movie_director = db.Column(db.String(100), nullable = False)
    release_year = db.Column(db.Integer, nullable = False)
    movie_rating = db.Column(db.Float, nullable = False)