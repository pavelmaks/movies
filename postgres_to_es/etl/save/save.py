from time import sleep
from etl.state.base_storage import BaseStorage
from datetime import datetime
from logger import logger
from typing import Generator
from decorators import coroutine
from settings import STATE_KEY
from etl.state.models import State, Movie

@coroutine
def save_movies(state: State) -> Generator[list[Movie], None, None]:
    while movies := (yield):
        logger.info(f'Received for saving {len(movies)} movies')
        print([movie.json() for movie in movies])
        state.set_state(STATE_KEY, str(movies[-1].modified))
