from data_manager_interface import DataManagerInterface
from flask_sqlalchemy import SQLAlchemy
from data_models import Movie, User, UserMovie

class SQLiteDataManager(DataManagerInterface):
    def __init__(self, db_file_name):
        self.db = SQLAlchemy(db_file_name)
        self.db.create_all()
    
    def get_all_movies(self):
        return self.db.session.query(Movie).all()
    
    def get_all_users(self):
        return self.db.session.query(User).all()
    
    def get_user_movies(self, user_id):
        return self.db.session.query(Movie.movie_name,UserMovie.watchlist_status, UserMovie.user_rating) \
        .join(UserMovie).filter(UserMovie.user_id == user_id).all()
    
    def add_user(self, user):
        user_data = User(**user)
        self.db.session.add(user_data)
        self.db.commit()
    
    def add_movie(self, movie):
        movie_data = Movie(**movie)
        self.db.session.add(movie_data)
        self.db.commit()
    
    def update_movie(self, movie):
        updated_movie = Movie(**movie)
        self.db.session.add(updated_movie)
        self.db.commit()
    
    def delete_movie(self, movie_id):
        movie_to_delete = self.db.session.query(Movie).filter(Movie.id == movie_id).first()
        self.db.session.delete(movie_to_delete)
        self.db.commit()
