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
    
    def get_all_users(self):
        return self.db.session.query(User).all()
    
    def get_user_movies(self, user_id):
        return self.db.session.query(Movie.movie_name,UserMovie.watchlist_status, UserMovie.user_rating) \
        .join(UserMovie).filter(UserMovie.user_id == user_id).all()
    
    def add_user(self, user):
        user_data = User(**user)
        self.db.session.add(user_data)
        self.db.commit()
    
    def add_movie(self, movie, user_id, watchlist_status, user_rating):
        movie_data = Movie(**movie)
        self.db.session.add(movie_data)
        self.db.commit()
        movie_id = movie_data.id
        user_movie_data = UserMovie(user_id=user_id, movie_id=movie_id, watchlist_status=watchlist_status, user_rating=user_rating)
        self.db.session.add(user_movie_data)
        self.db.commit()
    
    def update_movie(self, user_id, movie_id, rating, status):
        user_movie = self.db.session.query(UserMovie).filter(UserMovie.movie_id == movie_id, UserMovie.user_id == user_id).first
        if user_movie:
            user_movie.watchlist_status = status
            user_movie.user_rating = rating
            db.session.commit()
            return True  # Indicate success
        return False  # Indicate failure (movie not found)
    
    def delete_movie(self, user_id, movie_id):
        movie_to_delete = self.db.session.query(UserMovie).filter(UserMovie.movie_id == movie_id, UserMovie.user_id == user_id).first
        if movie_to_delete:
            self.db.session.delete(movie_to_delete)
            self.db.commit()
            return True
        return False
