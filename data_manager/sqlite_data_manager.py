from data_manager_interface import DataManagerInterface
from flask_sqlalchemy import SQLAlchemy
from data_models import Movie, User

class SQLiteDataManager(DataManagerInterface):
    def __init__(self, db_file_name):
        self.db = SQLAlchemy(db_file_name)