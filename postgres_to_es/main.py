from datetime import datetime
from time import sleep

import psycopg
from psycopg import ServerCursor
from psycopg.rows import dict_row

from decorators import backoff
from etl.extractors import fetch_changed_filmworks, fetch_changed_movies
from etl.save import save_movies
from etl.state.json_file_storage import JsonFileStorage
from etl.state.models import State
from etl.transform import transform_movies
from logger import logger
from settings import DSL, LAST_FILMWORK_KEY


@backoff()
def main():
    state = State(JsonFileStorage(logger=logger))

    with psycopg.connect(**DSL, row_factory=dict_row) as conn, ServerCursor(conn, 'fetcher') as cur:
        saver_coro = save_movies(state)
        transformer_coro = transform_movies(next_node=saver_coro)
        fetcher_coro_movies = fetch_changed_movies(cur, transformer_coro)
        fetcher_coro_filmworks = fetch_changed_filmworks(cur, fetcher_coro_movies)

        while True:
            logger.info('Starting ETL process for updates ...')
            fetcher_coro_filmworks.send(state.get_state(LAST_FILMWORK_KEY) or str(datetime.min))
            sleep(1)


if __name__ == '__main__':
    main()
