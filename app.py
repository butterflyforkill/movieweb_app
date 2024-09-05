import os
from flask import Flask, render_template, request, redirect
from data_manager.sqlite_data_manager import SQLiteDataManager

app = Flask(__name__)
db_path = os.path.join(os.getcwd(), 'data', 'movie_app.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
data_manager = SQLiteDataManager(app)

@app.route('/')
def home():
    movies = data_manager.get_all_movies()
    return render_template('index.html')


@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)


@app.route('/users/<int:user_id>')
def get_user_movies(user_id):
    user_movies = data_manager.get_user_movies(user_id)
    return user_movies


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['username']

        # Create a new user object
        user = {'user_name': username}

        # Add the user to the database
        data_manager.add_user(user)

        # Redirect to the users page or display a success message
        return redirect('/users', code=302)

    return render_template('add_user.html')


@app.route('/users/<user_id>/add_movie')
def add_movie(user_id):
    pass


@app.route('/users/<user_id>/update_movie/<movie_id>')
def update_movie(user_id, movie_id):
    pass


@app.route('/users/<user_id>/delete_movie/<movie_id>')
def delete_movie(user_id, movie_id):
    pass


if __name__ == '__main__':
    app.run(debug=True)