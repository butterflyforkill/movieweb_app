import os
import requests
from flask import Flask, render_template, request, redirect, url_for
from data_manager.sqlite_data_manager import SQLiteDataManager
from config.config_files import APIkeys

app = Flask(__name__)
db_path = os.path.join(os.getcwd(), 'data', 'movie_app.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
data_manager = SQLiteDataManager(app)

@app.route('/')
def home():
    movies = data_manager.get_all_movies()
    return render_template('index.html', movies=movies)


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


def response_parser(resp):
        """
        Parses the response from an HTTP request and
        returns the appropriate data or error message.

        Args:
        resp (requests.Response): The response object
            from the HTTP request.

        Returns:
        dict or str: If the response status code is OK
                    and the JSON response indicates success,
                    returns the JSON data.
                    If the JSON response indicates failure,
                    returns an error message.
                    If the response status code is not OK,
                    returns an error message with the status code.
        """
        if resp.status_code == requests.codes.ok:
            if resp.json()['Response'] == 'False':
                error_resp = resp.json()
                return f"Error: {error_resp['Error']}"
            else:
                return resp.json()
        else:
            return f"Error: {resp.status_code}"


@app.route('/users/<user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    if request.method == 'POST':
        movie_name = request.form['movie_name']
        watchlist_status = request.form['watchlist_status']
        user_rating = request.form.get('user_rating')
        api_url = f'http://www.omdbapi.com/?apikey={APIkeys.APIkey}&t={movie_name}'
        response = requests.get(api_url)
        parsed_resp = response_parser(response)
        if parsed_resp == 'Error: Movie not found!':
            print(f"The movie {movie_name} doesn't exist")
        elif type(parsed_resp) == str:
            print(parsed_resp)
        else:
            rating = float(parsed_resp['Ratings'][0]['Value'].split('/')[0])
            year_str = parsed_resp['Year'] 
            year = year_str[0:4]
            print(rating)
            movie = {
                
                'movie_poster':parsed_resp['Poster'],
                'movie_name': movie_name,
                'movie_director':parsed_resp['Director'],
                'release_year':year, 
                'movie_rating':rating
                }

            # Add the movie to the user's list
            data_manager.add_movie(movie, user_id, watchlist_status, user_rating)

        # Redirect to the user's movies page or display a success message
        return redirect(url_for('user_movies', user_id=user_id))

    # Render the form for GET requests
    return render_template('add_movie.html')


@app.route('/users/<user_id>/update_movie/<movie_id>')
def update_movie(user_id, movie_id):
    pass


@app.route('/users/<user_id>/delete_movie/<movie_id>')
def delete_movie(user_id, movie_id):
    pass


if __name__ == '__main__':
    app.run(debug=True)