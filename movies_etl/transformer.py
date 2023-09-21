from typing import Generator

from decorators import coroutine
from models.models import Movie
from settings import logger


@coroutine
def transform(next_node: Generator) -> Generator[list[dict], None, None]:
    while movie_dicts := (yield):
        batch = []
        for movie_dict in movie_dicts:
            movie = Movie(**movie_dict)
            logger.info(movie.json())

            batch.append(movie)
        next_node.send(batch)
