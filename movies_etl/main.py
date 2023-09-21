from datetime import datetime
from time import sleep

import backoff
import elastic_transport
import psycopg
from base_etl import BaseEtl
from elasticsearch import Elasticsearch
from indexes import genres_index, movies_index, persons_index
from models.models import Genre, Movie, Person
from psycopg import ServerCursor
from psycopg.conninfo import make_conninfo
from psycopg.rows import dict_row
from queries import genres, movies, persons
from settings import (
    STATE_GENRES_KEY,
    STATE_MOVIE_KEY,
    STATE_PERSONES_KEY,
    database_settings,
    es_settings,
    logger,
)
from state.json_file_storage import JsonFileStorage
from state.state import State


@backoff.on_exception(
    backoff.constant,
    (psycopg.OperationalError,
     elastic_transport.ConnectionError,
     elastic_transport.ConnectionTimeout)
)
def main():

    state = State(JsonFileStorage(logger=logger))

    host = es_settings.host
    es = Elasticsearch(hosts=[f'http://{host}:9200'])
    dsn = make_conninfo(**database_settings.dict())
    logger.info('Try connect to Postgres')
    with psycopg.connect(dsn, row_factory=dict_row) as conn, ServerCursor(conn, 'fetcher') as cur:
        movies_etl = BaseEtl(cur, es, state, movies_index, movies, Movie, STATE_MOVIE_KEY)
        genres_etl = BaseEtl(cur, es, state, genres_index, genres, Genre, STATE_GENRES_KEY)
        persons_etl = BaseEtl(cur, es, state, persons_index, persons, Person, STATE_PERSONES_KEY)
        while True:
            logger.info('Starting ETL process for updates ...')

            movies_etl()
            genres_etl()
            persons_etl()

            sleep(15)


if __name__ == '__main__':
    main()
