from data_manager.data_manager_interface import DataManagerInterface
from data_manager.data_models import db, Movie, User, UserMovie

class SQLiteDataManager(DataManagerInterface):
    def __init__(self, app):
        self.app = app
        self.db = db # sqlalchemy object from data_models
        db.init_app(app) # inizialisation of the db in the app
        with app.app_context():
            self.db.create_all() # create all the tables
    
    def get_all_movies(self):
        return self.db.session.query(Movie).all()
    
    def get_movie_by_id(self, movie_id):
        return self.db.session.query(Movie).filter(Movie.id == movie_id).first()
    
    def get_movie_by_name(self, movie_name):
        return self.db.session.query(Movie) \
            .filter(self.db.func.lower(Movie.movie_name) == self.db.func.lower(movie_name)).first()
    
    def get_movie_by_movie_by_user(self, movie_id, user_id):
        return self.db.session.query(UserMovie).filter(UserMovie.movie_id == movie_id, UserMovie.user_id == user_id).first()
    
    def get_movie_by_watch_status(self,user_id, watch_status):
        return self.db.session.query(UserMovie, Movie.movie_name, Movie.movie_poster) \
                .filter(UserMovie.user_id == user_id, UserMovie.watchlist_status == watch_status).join(Movie).all()

    def get_all_users(self):
        return self.db.session.query(User).all()
    
    def get_user_movies(self, user_id):
        return self.db.session.query(UserMovie, Movie.movie_name, Movie.movie_poster) \
            .filter(UserMovie.user_id == user_id) \
            .join(Movie).all()
    
    def add_user(self, user):
        user_data = User(**user)
        self.db.session.add(user_data)
        self.db.session.commit()
    
    def add_movie(self, movie, user_id, watchlist_status, user_rating):
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
        movie_to_delete = self.db.session.query(UserMovie).filter(UserMovie.movie_id == movie_id, UserMovie.user_id == user_id).first()
        if movie_to_delete:
            self.db.session.delete(movie_to_delete)
            self.db.session.commit()
            return True
        return False
