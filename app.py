import os
import requests
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from data_manager.sqlite_data_manager import SQLiteDataManager
from config.config_files import APIkeys

app = Flask(__name__)
db_path = os.path.join(os.getcwd(), 'data', 'movie_app.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SECRET_KEY'] = "your secret key"
data_manager = SQLiteDataManager(app)

@app.route('/', methods=['GET'])
def home():
    movies = data_manager.get_all_movies()
    return render_template('index.html', movies=movies)


@app.route('/movies/<int:movie_id>', methods=['GET'])
def movie_details(movie_id):
    movie = data_manager.get_movie_by_id(movie_id)
    return render_template('movie.html', movie=movie)

@app.route('/users', methods=['GET'])
def list_users():
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)


@app.route('/users/<int:user_id>',methods=['GET'])
def user_movies(user_id):
    user_movies = data_manager.get_user_movies(user_id)
    return render_template('user_movies.html', user_movies=user_movies)


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


@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
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
                'movie_rating':rating,
                'movie_plot': parsed_resp['Plot']
                }

            # Add the movie to the user's list
            data_manager.add_movie(movie, user_id, watchlist_status, user_rating)

        # Redirect to the user's movies page or display a success message
        return redirect(url_for('user_movies', user_id=user_id))

    # Render the form for GET requests
    return render_template('add_movie.html')


@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    try:
        user_movie = data_manager.get_movie_by_movie_by_user(movie_id, user_id)
        if user_movie is None:
            return "Movie not found or not in user's list.", 404

        if request.method == 'POST':
            # Extract the rating and status from the request data
            rating = int(request.form.get('rating'))
            status = request.form.get('status')

            # Update the movie using the data manager
            if data_manager.update_movie(user_id, movie_id, rating, status):
                return redirect(url_for('user_movies', user_id=user_id))
            else:
                return jsonify({'message': 'Movie not found or not in user\'s list'}), 404

        # Render the HTML form for updating the movie
        return render_template('update_movie.html', user_movie=user_movie)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>', methods = ['POST'])
def delete_movie(user_id, movie_id):
    try:
        if data_manager.delete_movie(user_id, movie_id):
            flash('Movie deleted successfully', 'success')
            return redirect(url_for('user_movies', user_id=user_id))
        else:
            flash('Movie not found or not associated with the user', 'error')
            return redirect(url_for('user_movies', user_id=user_id))
    except Exception as e:
        # Handle exceptions gracefully
        flash(f'An error occurred: {str(e)}', 'error')
        return redirect(url_for('user_movies', user_id=user_id))


if __name__ == '__main__':
    app.run(debug=True)