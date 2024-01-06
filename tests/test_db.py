import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from db import (
    create_database_connection,
    UserOperations,
    MovieOperations,
    UserBase,
)


def test_create_database_connection():
    assert create_database_connection() is not None


def test_user_operations():
    user_ops = UserOperations(create_database_connection())
    user = UserBase(username="test_user", password="test_password")
    user_ops.register_new_user(user)
    assert user_ops.authenticate_user("test_user", "test_password") is not None


def test_movie_operations():
    movie_ops = MovieOperations(create_database_connection())
    movie_ops.add_movie_for_user(1, "Test Movie")
    movies = movie_ops.get_movies_for_user(1)
    assert len(movies) == 1
    assert movies[0].title == "Test Movie"
    movie_ops.delete_movie_by_id(1, movies[0].id)
    assert len(movie_ops.get_movies_for_user(1)) == 0
