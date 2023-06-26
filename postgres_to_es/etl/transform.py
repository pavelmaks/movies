from datetime import datetime
from typing import Generator

from decorators import coroutine
from etl.state.models import Movie
from logger import logger


@coroutine
def transform_movies(next_node: Generator) -> Generator[list[dict], None, None]:
    """Валидирует данные по модели Movie"""
    while movie_dicts := (yield):
        batch = []
        for movie_dict in movie_dicts:
            movie = Movie(**movie_dict)
            movie.title = movie.title.upper()
            logger.info(movie.json())
            batch.append(movie)
        next_node.send(batch)
