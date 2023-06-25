# string = 'curl -XPUT http://127.0.0.1:9200/movies -H "Content-Type: application/json" -d'
from dataclasses import astuple
from datetime import datetime
from time import sleep
from typing import Coroutine, Generator

import psycopg
from psycopg import ServerCursor
from psycopg.conninfo import make_conninfo
from psycopg.rows import dict_row

from logger import logger
from etl.extract.base_extractor import fetch_changed_movies
from etl.save.save import save_movies
from etl.transform.transform import transform_movies
from decorators import backoff
from settings import DSL, STATE_KEY
from etl.state.json_file_storage import JsonFileStorage
from etl.state.models import State, Movie


@backoff()
def main():
    state = State(JsonFileStorage(logger=logger))

    with psycopg.connect(**DSL, row_factory=dict_row) as conn, ServerCursor(conn, 'fetcher') as cur:
        saver_coro = save_movies(state)
        transformer_coro = transform_movies(next_node=saver_coro)
        fetcher_coro = fetch_changed_movies(cur, transformer_coro)

        while True:
            last_movies_updated = state.get_state(STATE_KEY)
            logger.info('Starting ETL process for updates ...')

            fetcher_coro.send(state.get_state(STATE_KEY) or str(datetime.min))

            sleep(1)


if __name__ == '__main__':
    main()
