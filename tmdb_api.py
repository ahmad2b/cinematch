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
    backdrop_path: str
    genre_ids: List[int]
    id: int
    original_language: str
    original_title: str
    overview: str
    popularity: float
    poster_path: str
    release_date: Optional[str]
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


# {
#     "endpoints": [
#         {
#             "name": "certification",
#             "description": "Filter results by movie certification.",
#             "type": "string",
#             "example": "US:PG-13",
#         },
#         {
#             "name": "certification.gte",
#             "description": "Filter results by minimum movie certification.",
#             "type": "string",
#             "example": "US:PG-13",
#         },
#         {
#             "name": "certification.lte",
#             "description": "Filter results by maximum movie certification.",
#             "type": "string",
#             "example": "US:PG-13",
#         },
#         {
#             "name": "certification_country",
#             "description": "Filter results by movie certification country.",
#             "type": "string",
#             "example": "US",
#         },
#         {
#             "name": "include_adult",
#             "description": "Include adult movies in the results.",
#             "type": "boolean",
#             "example": "false",
#         },
#         {
#             "name": "include_video",
#             "description": "Include movies with a Trailer, Teaser, Clip, Featurette, or Behind the Scenes video in the results.",
#             "type": "boolean",
#             "example": "false",
#         },
#         {
#             "name": "language",
#             "description": "Specify a language to localize the results.",
#             "type": "string",
#             "example": "en-US",
#         },
#         {
#             "name": "page",
#             "description": "Specify the page of results to return.",
#             "type": "int32",
#             "example": "1",
#         },
#         {
#             "name": "primary_release_year",
#             "description": "Filter results by the original release year.",
#             "type": "int32",
#             "example": "2020",
#         },
#         {
#             "name": "primary_release_date.gte",
#             "description": "Filter results by the minimum original release date.",
#             "type": "date",
#             "example": "2020-01-01",
#         },
#         {
#             "name": "primary_release_date.lte",
#             "description": "Filter results by the maximum original release date.",
#             "type": "date",
#             "example": "2020-12-31",
#         },
#         {
#             "name": "region",
#             "description": "Specify a region to filter results from.",
#             "type": "string",
#             "example": "US",
#         },
#         {
#             "name": "release_date.gte",
#             "description": "Filter results by the minimum release date.",
#             "type": "date",
#             "example": "2020-01-01",
#         },
#         {
#             "name": "release_date.lte",
#             "description": "Filter results by the maximum release date.",
#             "type": "date",
#             "example": "2020-12-31",
#         },
#         {
#             "name": "sort_by",
#             "description": "Specify the sort order of the results.",
#             "type": "string",
#             "example": "popularity.desc",
#         },
#         {
#             "name": "vote_average.gte",
#             "description": "Filter results by the minimum vote average.",
#             "type": "float",
#             "example": "7.0",
#         },
#         {
#             "name": "vote_average.lte",
#             "description": "Filter results by the maximum vote average.",
#             "type": "float",
#             "example": "9.0",
#         },
#         {
#             "name": "vote_count.gte",
#             "description": "Filter results by the minimum number of votes.",
#             "type": "float",
#             "example": "100",
#         },
#         {
#             "name": "vote_count.lte",
#             "description": "Filter results by the maximum number of votes.",
#             "type": "float",
#             "example": "1000",
#         },
#         {
#             "name": "watch_region",
#             "description": "Specify a watch region to filter results from.",
#             "type": "string",
#             "example": "US",
#         },
#         {
#             "name": "with_cast",
#             "description": "Filter results by cast members.",
#             "type": "string",
#             "example": "Leonardo DiCaprio",
#         },
#         {
#             "name": "with_companies",
#             "description": "Filter results by production companies.",
#             "type": "string",
#             "example": "Walt Disney Pictures",
#         },
#         {
#             "name": "with_crew",
#             "description": "Filter results by crew members.",
#             "type": "string",
#             "example": "Steven Spielberg",
#         },
#         {
#             "name": "with_genres",
#             "description": "Filter results by genres.",
#             "type": "string",
#             "example": "Action",
#         },
#         {
#             "name": "with_keywords",
#             "description": "Filter results by keywords.",
#             "type": "string",
#             "example": "love",
#         },
#         {
#             "name": "with_origin_country",
#             "description": "Filter results by the original country of production.",
#             "type": "string",
#             "example": "US",
#         },
#         {
#             "name": "with_original_language",
#             "description": "Filter results by the original language of the movie.",
#             "type": "string",
#             "example": "en",
#         },
#         {
#             "name": "with_people",
#             "description": "Filter results by people involved in the movie.",
#             "type": "string",
#             "example": "Leonardo DiCaprio",
#         },
#         {
#             "name": "with_release_type",
#             "description": "Filter results by the release type.",
#             "type": "int32",
#             "example": "2",
#         },
#         {
#             "name": "with_runtime.gte",
#             "description": "Filter results by the minimum runtime.",
#             "type": "int32",
#             "example": "90",
#         },
#         {
#             "name": "with_runtime.lte",
#             "description": "Filter results by the maximum runtime.",
#             "type": "int32",
#             "example": "120",
#         },
#         {
#             "name": "with_watch_monetization_types",
#             "description": "Filter results by the monetization types available.",
#             "type": "string",
#             "example": "flatrate",
#         },
#         {
#             "name": "with_watch_providers",
#             "description": "Filter results by the watch providers available.",
#             "type": "string",
#             "example": "Netflix",
#         },
#         {
#             "name": "without_companies",
#             "description": "Filter results by excluding production companies.",
#             "type": "string",
#             "example": "Warner Bros.",
#         },
#         {
#             "name": "without_genres",
#             "description": "Filter results by excluding genres.",
#             "type": "string",
#             "example": "Action",
#         },
#         {
#             "name": "without_keywords",
#             "description": "Filter results by excluding keywords.",
#             "type": "string",
#             "example": "love",
#         },
#         {
#             "name": "without_watch_providers",
#             "description": "Filter results by excluding watch providers.",
#             "type": "string",
#             "example": "Netflix",
#         },
#         {
#             "name": "year",
#             "description": "Filter results by the release year.",
#             "type": "int32",
#             "example": "2020",
#         },
#     ]
# }
