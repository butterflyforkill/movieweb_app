from data_manager_interface import DataManagerInterface
from flask_sqlalchemy import SQLAlchemy
from data_models import Movie, User

class SQLiteDataManager(DataManagerInterface):
    def __init__(self, db_file_name):
        self.db = SQLAlchemy(db_file_name)
        self.db.create_all()
    
    def get_all_users(self):
        return self.db.session.query(User).all()
    
    def get_user_movies(self, user_id):
        pass
    
    def add_user(self, user):
        user_data = User(**user)
        self.db.session.add(user_data)
        self.db.commit()
    
    def add_movie(self, movie):
        user_data = User(**movie)
        self.db.session.add(user_data)
        self.db.commit()
    
    def update_movie(self, movie):
        pass
    
    def delete_movie(self, movie_id):
        pass
