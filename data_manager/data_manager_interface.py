from abc import ABC, abstractmethod

class DataManagerInterface(ABC):

    @abstractmethod
    def get_all_users(self):
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        pass
    
    @abstractmethod
    def add_user(user):
        pass
    
    @abstractmethod
    def add_movie(movie):
        pass
    
    @abstractmethod
    def update_movie(movie):
        pass
    
    @abstractmethod
    def delete_movie(movie_id):
        pass
