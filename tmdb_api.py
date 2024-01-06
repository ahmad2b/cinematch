# Import the required libraries
import streamlit as st
import requests as req
from typing import List, Dict, Any, Optional
from datetime import datetime
import aiohttp
import asyncio
from pydantic import BaseModel, validator


class Movie(BaseModel):
    """Movie class with attributes that match the structure of a movie object in the TMDB API"""

    adult: bool
    backdrop_path: Optional[str] = None
    genre_ids: List[int]
    id: int
    original_language: str
    original_title: str
    overview: str
    popularity: float
    poster_path: str
    release_date: str = ""
    title: str
    video: bool
    vote_average: float
    vote_count: int

    @validator("vote_average")
    def validate_vote_average(cls, v: float):
        if v < 0 or v > 10:
            raise ValueError("vote_average must be between 0 and 10")
        return v


class MovieResponse(BaseModel):
    """MovieResponse class to handle the structure of a response from the TMDB API when requesting movies"""

    page: int
    results: List[Movie]
    total_pages: int
    total_results: int


class Genre(BaseModel):
    """Genre class to handle the structure of a genre object in the TMDB API"""

    id: int
    name: str


class GenresResponse(BaseModel):
    """GenresResponse class to handle the structure of a response from the TMDB API when requesting genres"""

    genres: List[Genre]


# MovieDB class to interact with the TMDB API
class MovieDB:
    def __init__(self) -> None:
        self.api_key: str = st.secrets["tmdb_apikey"]
        self.access_token: str = st.secrets["tmdb_accesstoken"]
        self.base_url: str = "https://api.themoviedb.org/3/"
        if self.api_key is None or self.access_token is None:
            raise Exception(
                "API_KEY or ACCESS_TOKEN is not set in the secrets.toml file"
            )

    def discover_movies(self) -> MovieResponse:
        url: str = f"{self.base_url}/discover/movie?api_key={self.api_key}"
        response = req.get(url)
        data: Dict[str, Any] = response.json()
        return MovieResponse(
            page=data["page"],
            results=[Movie(**movie) for movie in data["results"]],
            total_pages=data["total_pages"],
            total_results=data["total_results"],
        )

    def get_movie_genres(self) -> GenresResponse:
        url: str = f"{self.base_url}genre/movie/list?language=en&api_key={self.api_key}"
        response = req.get(url)
        data: Dict[str, Any] = response.json()
        return GenresResponse(genres=[Genre(**genre) for genre in data["genres"]])

    async def search_movies_by_keywords(self, keywords: List[str]) -> List[Movie]:
        print("search_movies_by_keywords", keywords)
        async with aiohttp.ClientSession() as session:
            tasks = [self.search_movies(session, keyword) for keyword in keywords]
            all_movies = await asyncio.gather(*tasks)
        return [movie for sublist in all_movies for movie in sublist]

    async def search_movies(self, session, keyword: str) -> List[Movie]:
        url: str = f"{self.base_url}search/movie?query={keyword}&api_key={self.api_key}"
        async with session.get(url) as response:
            data: Dict[str, Any] = await response.json()
        return [Movie(**movie) for movie in data["results"]]

    def create_query(self, params: Dict[str, str]) -> str:
        query = "&".join(
            f"{key}={value.replace(' ', '+')}" for key, value in params.items()
        )
        return query

    def discover_movies_with_params(self, params) -> MovieResponse:
        query = self.create_query(params)
        url = f"{self.base_url}discover/movie?api_key={self.api_key}&{query}"
        print("url: ", url)
        response = req.get(url)
        data = response.json()
        print("data: ", data["results"])
        return MovieResponse(
            page=data["page"],
            results=[Movie(**movie) for movie in data["results"]],
            total_pages=data["total_pages"],
            total_results=data["total_results"],
        )
