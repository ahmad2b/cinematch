import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
from typing import Dict
from sqlalchemy.exc import IntegrityError
from sqlalchemy import inspect
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

# Define the base class using declarative_base
Base = declarative_base()


def create_database_connection():
    """
    This function creates a connection to the database using the credentials stored in the secrets.
    """
    username = st.secrets["DATABASE_USERNAME"]
    password = st.secrets["DATABASE_PASSWORD"]
    dbname = st.secrets["DATABASE_NAME"]
    port = st.secrets["DATABASE_PORT"]
    host = st.secrets["DATABASE_HOST"]

    # Create database engine
    engine = create_engine(
        f"postgresql://{username}:{password}@{host}:{port}/{dbname}",
        # echo=True,
    )
    return engine


class UserEntity(Base):  # type: ignore
    """
    This class represents the User entity in the database.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(
        String,
        nullable=False,
        unique=True,
    )
    password = Column(String, nullable=False)
    movies = relationship("MovieEntity", backref="user")

    def set_password(self, password):
        """
        This method hashes the password and stores it in the password field.
        """
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """
        This method checks if the provided password matches the hashed password stored in the database.
        """
        return check_password_hash(self.password, password)


class UserOperations:
    """
    This class handles operations related to the User entity.
    """

    def __init__(self, engine):
        self.engine = engine
        self.Session = sessionmaker(bind=self.engine)
        if not inspect(self.engine).has_table("users"):
            Base.metadata.create_all(self.engine)

    def register_new_user(self, username, password):
        """
        This method registers a new user in the database.
        """
        session = self.Session()

        existing_user = session.query(UserEntity).filter_by(username=username).first()

        # Check if the user already exists
        if existing_user:
            session.close()
            return {"status": "error", "message": "Username already exists"}

        # Create a new user
        try:
            user = UserEntity(username=username)
            user.set_password(password)
            session.add(user)
            session.commit()
            session.close()
            return {
                "status": "success",
                "message": "User created successfully. Please login to continue.",
                "user": user,
            }
        except IntegrityError:
            session.rollback()
            return {"status": "error", "message": "Username already exists"}
        finally:
            session.close()

    def authenticate_user(self, username, password):
        """
        This method authenticates a user by checking the username and password.
        """
        session = self.Session()
        user = session.query(UserEntity).filter_by(username=username).first()

        # Check if the user exists and the password is correct
        if user and user.check_password(password):
            session.close()
            # print("Login successful", user.id)
            return {"status": "success", "message": "Login successful", "user": user}
        else:
            session.close()
            return {"status": "error", "message": "Invalid username or password"}


class MovieEntity(Base):  # type: ignore
    """
    This class represents the Movie entity in the database.
    """

    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    image = Column(String, nullable=True)
    user_id = Column(
        Integer, ForeignKey("users.id"), nullable=False
    )  # Add ForeignKey here


class MovieOperations:
    """
    This class handles operations related to the Movie entity.
    """

    def __init__(self, engine):
        self.engine = engine
        self.Session = sessionmaker(bind=self.engine)
        if not inspect(self.engine).has_table("movies"):
            Base.metadata.create_all(self.engine)

    def add_movie_for_user(self, user_id, title, image=None):
        """
        This method adds a new movie for a user in the database.
        """
        session = self.Session()
        movie = MovieEntity(user_id=user_id, title=title, image=image)
        session.add(movie)
        session.commit()
        session.close()

    def get_movies_for_user(self, user_id):
        """
        This method retrieves all movies for a user from the database.
        """
        session = self.Session()
        movies = session.query(MovieEntity).filter_by(user_id=user_id).all()
        session.close()
        return movies

    def delete_movie_by_id(self, movie_id):
        """
        This method deletes a movie by its id from the database.
        """
        session = self.Session()
        movie = session.query(MovieEntity).filter_by(id=movie_id).first()
        if movie:
            session.delete(movie)
            session.commit()
        session.close()
