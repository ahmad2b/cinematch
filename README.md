# Cinematch: AI Movie Recommendation Engine

Cinematch is an interactive movie recommendation system built using Streamlit and the OpenAI API. It leverages the power of AI to provide personalized movie recommendations based on user preferences.

## Features

- **User Interface**: Create a user-friendly interface for users to input their movie preferences and ratings.
- **Database Connectivity**: Use database connectivity to fetch and display movie recommendations, along with relevant details such as genre, director, actors, etc.
- **Secrets Management**: Implement secrets management to securely store and access API keys for interacting with the movie database.
- **Deployment**: Deploy the application on a cloud platform such as Heroku for easy access.

## Tech Stack

This project uses the following technologies:

- **OpenAI API**: Used for AI functionalities.
- **TMDB API**: An API for fetching movie data.

- **Python**: The main programming language.
- **Streamlit**: A Python library for creating web interfaces.
- **Requests and aiohttp**: Python libraries for making HTTP requests.
- **Pydantic**: A Python library for data validation and settings management.
- **PostgreSQL (supabase)**: The database system.
- **SQLAlchemy**: A Python SQL toolkit and ORM library.
- **pytest**: A testing framework for Python.
- **Git**: The version control system.
- **Streamlit Cloud**: The cloud platform for deploying our Streamlit application.

## Table of Contents

- [Cinematch: AI Movie Recommendation Engine](#cinematch-ai-movie-recommendation-engine)
  - [Features](#features)
  - [Tech Stack](#tech-stack)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
  - [License](#license)

## Installation

This project requires Python 3.8 or later. Clone the repository and install the dependencies:

```sh
git clone https://github.com/ahmad2b/Cinematch.git
cd Cinematch
pip install -r requirements.txt
```

## Usage

To start the application, run the following command in your terminal:

```sh
streamlit run Home.py
```

Then, open your web browser and navigate to `http://localhost:8501` to start using Cinematch.

## License

This project is licensed under the terms of the MIT license. See LICENSE for additional details.

---
