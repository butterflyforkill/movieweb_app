from abc import ABC, abstractmethod

class DataManagerInterface(ABC):
    """
    Interface for data management operations.

    This interface defines the methods that a data manager 
    class must implement to handle user and movie data.
    """

    @abstractmethod
    def get_all_users(self):
        """
        Retrieves all users from the data source.

        Returns:
            A list of user objects.
        """
        pass

    @abstractmethod
    def get_all_movies(self):
        """
        Retrieves all movies from the data source.

        Returns:
            A list of movie objects.
        """
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        """
        Retrieves all movies associated with a specific user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            A list of movie objects.
        """
        pass

    @abstractmethod
    def add_user(self, user):
        """
        Adds a new user to the data source.

        Args:
            user: A user object.
        """
        pass

    @abstractmethod
    def add_movie(self, movie, user_id, watchlist_status, user_rating):
        """
        Adds a new movie to the data source, associated with a specific user.

        Args:
            movie: A movie object.
            user_id (int): The ID of the user.
            watchlist_status (bool): Whether the movie is on the user's watchlist.
            user_rating (int): The user's rating for the movie.
        """
        pass

    @abstractmethod
    def update_movie(self, user_id, movie_id, rating, status):
        """
        Updates the rating and watchlist status of a movie for a specific user.

        Args:
            user_id (int): The ID of the user.
            movie_id (int): The ID of the movie.
            rating (int): The new rating for the movie.
            status (bool): The new watchlist status for the movie.
        """
        pass

    @abstractmethod
    def delete_movie(self, movie_id):
        """
        Deletes a movie from the data source.

        Args:
            movie_id (int): The ID of the movie.
        """
        pass