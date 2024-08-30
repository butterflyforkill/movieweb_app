from data_manager_interface import DataManagerInterface
from flask_sqlalchemy import SQLAlchemy

class SQLiteDataManager(DataManagerInterface):
    def __init__(self, db_file_name):
        self.db = SQLAlchemy(db_file_name)