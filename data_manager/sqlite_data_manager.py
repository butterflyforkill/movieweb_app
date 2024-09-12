from data_manager.data_manager_interface import DataManagerInterface
from data_manager.data_models import db, Movie, User, UserMovie

class SQLiteDataManager(DataManagerInterface):
    """
    SQLite implementation of the DataManager interface for user and movie data.

    This class provides methods to interact with 
    a SQLite database to manage users and their movie lists.
    """
    def __init__(self, app):
        """
        Initializes the data manager with the Flask application.

        Args:
            app (Flask): The Flask application instance.
        """
        self.app = app
        self.db = db # sqlalchemy object from data_models
        db.init_app(app) # inizialisation of the db in the app
        with app.app_context():
            self.db.create_all() # create all the tables
    
    def get_all_movies(self):
        """
        Retrieves all movies from the database.

        Returns:
            list: A list of Movie objects.
        """
        return self.db.session.query(Movie).all()
    
    def get_movie_by_id(self, movie_id):
        """
        Retrieves a movie by its ID from the database.

        Args:
            movie_id (int): The ID of the movie.

        Returns:
            Movie: A Movie object or None if the movie is not found.
        """
        return self.db.session.query(Movie).filter(Movie.id == movie_id).first()
    
    def get_movie_by_name(self, movie_name):
        """
        Retrieves a movie by its name from the database (case-insensitive).

        Args:
            movie_name (str): The name of the movie.

        Returns:
            Movie: A Movie object or None if the movie is not found.
        """
        return self.db.session.query(Movie) \
            .filter(self.db.func.lower(Movie.movie_name) == self.db.func.lower(movie_name)).first()
    
    def get_movie_by_movie_by_user(self, movie_id, user_id):
        """
        Retrieves a UserMovie object representing a specific user's association with a movie.

        Args:
            movie_id (int): The ID of the movie.
            user_id (int): The ID of the user.

        Returns:
            UserMovie: A UserMovie object or None if the association is not found.
        """
        return self.db.session.query(UserMovie).filter(UserMovie.movie_id == movie_id, UserMovie.user_id == user_id).first()
    
    def get_movie_by_watch_status(self,user_id, watch_status):
        """
        Retrieves a list of movies associated with a user, filtered by watchlist status.

        Args:
            user_id (int): The ID of the user.
            watch_status (str): The watchlist status to filter by (e.g., 'watched', 'watching', 'wishlist').

        Returns:
            list: A list of tuples containing UserMovie objects, movie names, and movie posters.
        """
        return self.db.session.query(UserMovie, Movie.movie_name, Movie.movie_poster) \
                .filter(UserMovie.user_id == user_id, UserMovie.watchlist_status == watch_status).join(Movie).all()

    def get_all_users(self):
        """
        Retrieves all users from the database.

        Returns:
            list: A list of User objects.
        """
        return self.db.session.query(User).all()
    
    def get_user_movies(self, user_id):
        """
        Retrieves all movies associated with a user, including their names and posters.

        Args:
            user_id (int): The ID of the user.

        Returns:
            list: A list of tuples containing UserMovie objects, movie names, and movie posters.
        """
        return self.db.session.query(UserMovie, Movie.movie_name, Movie.movie_poster) \
            .filter(UserMovie.user_id == user_id) \
            .join(Movie).all()
    
    def add_user(self, user):
        user_data = User(**user)
        self.db.session.add(user_data)
        self.db.session.commit()
    
    def add_movie(self, movie, user_id, watchlist_status, user_rating):
        """
        Adds a movie to a user's list.

        Args:
            movie (dict): A dictionary containing movie data (expected keys: 'movie_name', etc.).
            user_id (int): The ID of the user.
            watchlist_status (str): The watchlist status for the movie (e.g., 'watched', 'watching', 'wishlist').
            user_rating (int, optional): The user's rating for the movie (between 1 and 5).

        Returns:
            None
        """
        existing_movie = self.db.session.query(Movie).filter_by(movie_name=movie['movie_name']).first()
        movie_data = Movie(**movie)

        if existing_movie:
            # Check if the user has already added this movie
            existing_user_movie = self.db.session.query(UserMovie).filter_by(user_id=user_id, movie_id=existing_movie.id).first()
            movie_id = existing_movie.id # if the movie alredy exists

            if existing_user_movie:
                # Movie already added by the user
                return
        else:
            self.db.session.add(movie_data)
            self.db.session.commit()
            movie_id = movie_data.id # if the movie was added to the database

        user_movie_data = UserMovie(user_id=user_id, movie_id=movie_id, watchlist_status=watchlist_status, user_rating=user_rating)
        self.db.session.add(user_movie_data)
        self.db.session.commit()
    
    def update_movie(self, user_id, movie_id, rating, status):
        """
        Updates the watchlist status and rating for a movie in a user's list.

        Args:
            user_id (int): The ID of the user.
            movie_id (int): The ID of the movie.
            rating (int): The new rating for the movie (between 1 and 5).
            status (str): The new watchlist status for the movie (e.g., 'watched', 'watching', 'wishlist').

        Raises:
            ValueError: If the rating is invalid (not an integer between 1 and 5) or the status is invalid.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        if not isinstance(rating, int) or int(rating) <= 1 or int(rating) >= 5:
            raise ValueError("Invalid rating: Rating must be an integer between 1 and 5.")

        if status not in ('watched', 'watching', 'wishlist'):
            raise ValueError("Invalid status: Status must be 'watched', 'watching', or 'wishlist'.")

        try:
            user_movie = self.get_movie_by_movie_by_user(movie_id, user_id)
            print(user_movie)
            if user_movie:
                user_movie.watchlist_status = status
                user_movie.user_rating = rating
                self.db.session.commit()
                return True  # Indicate success
            return False  # Indicate failure (movie not found)
        except Exception as e:
            # Handle exceptions gracefully
            raise ValueError(f"Error updating movie: {str(e)}")
    
    def delete_movie(self, user_id, movie_id):
        """
        Deletes a movie from a user's list.

        Args:
            user_id (int): The ID of the user.
            movie_id (int): The ID of the movie.

        Returns:
            bool: True if the deletion was successful, False otherwise.
        """
        movie_to_delete = self.db.session.query(UserMovie).filter(UserMovie.movie_id == movie_id, UserMovie.user_id == user_id).first()
        if movie_to_delete:
            self.db.session.delete(movie_to_delete)
            self.db.session.commit()
            return True
        return False
