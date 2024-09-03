import os
from flask import Flask
from data_manager.sqlite_data_manager import SQLiteDataManager

app = Flask(__name__)
db_path = os.path.join(os.getcwd(), 'data', 'movie_app.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
data_manager = SQLiteDataManager(app)

@app.route('/')
def home():
    return "Welcome to MovieWeb App!"


if __name__ == '__main__':
    app.run(debug=True)