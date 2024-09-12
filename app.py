import os
import requests
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from data_manager.sqlite_data_manager import SQLiteDataManager
from config.config_files import APIkeys
from utils.errors import NotFoundError, handle_internal_server_error

app = Flask(__name__)
db_path = os.path.join(os.getcwd(), 'data', 'movie_app.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SECRET_KEY'] = "your secret key"
data_manager = SQLiteDataManager(app)

@app.route('/', methods=['GET'])
def home():
    """
    Handles the home page request.

    Returns:
        The rendered index.html template with a list of all movies.
    """
    try:
        movies = data_manager.get_all_movies()
        return render_template('index.html', movies=movies)
    except Exception as e:
        flash(f'An error occurred while retrieving movies: {str(e)}', 'error')
        return render_template('index.html', movies=[])


@app.route('/<int:movie_id>', methods=['GET'])
def movie_details(movie_id):
    """
    Handles requests for individual movie details.

    Args:
        movie_id (int): The ID of the movie to retrieve.

    Returns:
        The rendered movie.html template with the movie details.
        Raises a NotFoundError if the movie is not found.
    """
    try:
        movie = data_manager.get_movie_by_id(movie_id)
        if movie is None:
            raise NotFoundError(f"Movie with ID {movie_id} not found")
        return render_template('movie.html', movie=movie)
    except NotFoundError as e:
        flash(str(e), 'error')
        return redirect(url_for('home'))
    except Exception as e:
        return handle_internal_server_error(app, e)


@app.route('/users', methods=['GET'])
def list_users():
    """
    Handles requests for a list of all users.

    Returns:
        The rendered users.html template with a list of users.
    """
    try:
        users = data_manager.get_all_users()
        return render_template('users.html', users=users)
    except Exception as e:
        return handle_internal_server_error(app, e)


@app.route('/users/<int:user_id>',methods=['GET'])
def user_movies(user_id):
    """
    Handles requests for a user's movies.

    Args:
        user_id (int): The ID of the user.

    Returns:
        The rendered user_movies.html template with the user's movies.
    """
    try:
        user_movies = data_manager.get_user_movies(user_id)
        return render_template('user_movies.html', user_movies=user_movies)
    except Exception as e:
        return handle_internal_server_error(app, e)


@app.route('/users/<int:user_id>/sort', methods=['POST'])
def movies_sort(user_id):
    """
    Handles requests for sorting a user's movies based on watch status.

    Args:
        user_id (int): The ID of the user.

    Returns:
        The rendered user_movies.html template with the sorted movies.
    """
    try:
        watch_status = request.form.get('watch_status')
        if watch_status:
            movies = data_manager.get_movie_by_watch_status(user_id, watch_status)
        else:
            movies = data_manager.get_user_movies(user_id)

        return render_template('user_movies.html', user_movies=movies)
    except Exception as e:
        # Handle the exception here
        print(f"An error occurred: {e}")
        flash("An error occurred while sorting movies.", "error")
        return redirect(url_for('user_movies', user_id=user_id))


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """
    Handles requests for adding a new user.

    Returns:
        The rendered add_user.html template if the request is a GET.
        Redirects to the users page if the request 
        is a POST and the user is successfully added.
    """
    if request.method == 'POST':
        username = request.form['username']

        # Create a new user object
        user = {'user_name': username}

        # Add the user to the database
        try:
            data_manager.add_user(user)
            return redirect('/users', code=302)
        except Exception as e:
            return handle_internal_server_error(app, e)

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
    """
    Handles requests for adding a new movie to a user's list.

    Args:
        user_id (int): The ID of the user.

    Returns:
        The rendered add_movie.html template for GET requests.
        Redirects to the user_movies page if the request 
        is a POST and the movie is successfully added.
    """
    if request.method == 'POST':
        movie_name = request.form['movie_name']
        watchlist_status = request.form['watchlist_status']
        user_rating = request.form.get('user_rating')
        api_url = f'http://www.omdbapi.com/?apikey={APIkeys.APIkey}&t={movie_name}'

        try:
            response = requests.get(api_url)
            parsed_resp = response_parser(response)

            if parsed_resp == 'Error: Movie not found!':
                flash(f"The movie {movie_name} doesn't exist", 'warning')
            elif type(parsed_resp) == str:
                flash(parsed_resp, 'error')
            else:
                try:
                    rating = 0
                    if parsed_resp['Ratings'] == []:
                        reting = 0.0
                    else:
                        rating = float(parsed_resp['Ratings'][0]['Value'].split('/')[0])
                    year_str = parsed_resp['Year']
                    year = year_str[0:4]

                    movie = {
                        'movie_poster': parsed_resp['Poster'],
                        'movie_name': movie_name,
                        'movie_director': parsed_resp['Director'],
                        'release_year': year,
                        'movie_rating': rating,
                        'movie_plot': parsed_resp['Plot']
                    }

                    # Add the movie to the user's list (handle potential data errors)
                    try:
                        data_manager.add_movie(movie, user_id, watchlist_status, user_rating)
                        return redirect(url_for('user_movies', user_id=user_id))
                    except Exception as e:
                        flash(f"An error occurred while adding the movie: {str(e)}", 'error')
                        return render_template('add_movie.html')

                except (ValueError, KeyError) as e:
                    flash(f"Invalid data in API response: {str(e)}", 'error')
                    return render_template('add_movie.html')

        except requests.exceptions.RequestException as e:
            # Handle any errors during the API request
            return handle_internal_server_error(app, e)

    # Render the form for GET requests
    return render_template('add_movie.html')


@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    """
    Handles requests for updating a movie in a user's list.

    Args:
        user_id (int): The ID of the user.
        movie_id (int): The ID of the movie to update.

    Returns:
        The rendered update_movie.html template for GET 
        requests with pre-filled user movie data.
        Redirects to the user_movies page if the request 
        is a POST and the movie is successfully updated.
    """
    try:
        user_movie = data_manager.get_movie_by_movie_by_user(movie_id, user_id)
        if user_movie is None:
            raise NotFoundError("Movie not found or not in user's list")

        if request.method == 'POST':
            # Extract the rating and status from the request data
            try:
                rating = int(request.form.get('rating'))
                status = request.form.get('status')

                # Update the movie using the data manager
                if data_manager.update_movie(user_id, movie_id, rating, status):
                    return redirect(url_for('user_movies', user_id=user_id))
                else:
                    # Use custom error
                    raise NotFoundError("Movie not found or not in user's list")
            except ValueError:
                flash("Invalid rating. Please enter a valid integer.", "error")
                return render_template('update_movie.html', user_movie=user_movie)

        # Render the HTML form for updating the movie
        return render_template('update_movie.html', user_movie=user_movie)
    except NotFoundError as e:
        flash(str(e), 'error')
        return redirect(url_for('user_movies', user_id=user_id))
    except Exception as e:
        return handle_internal_server_error(app, e)  # Handle unexpected errors


@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>', methods = ['POST'])
def delete_movie(user_id, movie_id):
    """
    Deletes a movie from a user's list.

    Args:
        user_id (int): The ID of the user.
        movie_id (int): The ID of the movie.

    Returns:
        Redirect to the user's movie list if successful, 
        or to the user's movie list with an error message if unsuccessful.
    """
    try:
        if data_manager.delete_movie(user_id, movie_id):
            flash('Movie deleted successfully', 'success')
            return redirect(url_for('user_movies', user_id=user_id))
        else:
            raise NotFoundError("Movie not found or not associated with the user")
    except NotFoundError as e:
        flash(str(e), 'error')
        return redirect(url_for('user_movies', user_id=user_id))
    except Exception as e:
        return handle_internal_server_error(app, e)


if __name__ == '__main__':
    app.run(debug=True)