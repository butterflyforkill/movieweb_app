from abc import ABC, abstractmethod

class DataManagerInterface(ABC):
    @abstractmethod
    def get_all_users(self):
        pass
    
    @abstractmethod
    def get_all_movies(self):
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        pass
    
    @abstractmethod
    def add_user(self, user):
        pass
    
    @abstractmethod
    def add_movie(self, movie, user_id, watchlist_status, user_rating):
        pass
    
    @abstractmethod
    def update_movie(self, user_id, movie_id, rating, status):
        pass
    
    @abstractmethod
    def delete_movie(self, movie_id):
        pass
