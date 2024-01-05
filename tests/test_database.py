from ..database import db_connect, UserManager, MovieManager


def test_add_movie():
    # Setup
    db = Database()
    # Exercise
    db.add_movie(user_id=1, title="Test Movie")
    # Verify
    movies = db.get_movies(user_id=1)
    assert len(movies) == 1
    assert movies[0].title == "Test Movie"
    # Teardown is handled by pytest
