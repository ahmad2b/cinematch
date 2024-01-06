import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tmdb_api import MovieDB


def test_movie_db():
    movie_db = MovieDB()
    movies = movie_db.get_popular_movies()
    assert len(movies) > 0
    genres = movie_db.get_genres()
    assert len(genres) > 0
