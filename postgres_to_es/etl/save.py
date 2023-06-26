from datetime import datetime
from time import sleep
from typing import Any, Generator

from elasticsearch import Elasticsearch
from elasticsearch.helpers import BulkIndexError, bulk

from decorators import coroutine
from es_schema import request_body
from etl.state.base_storage import BaseStorage
from etl.state.models import Movie, State
from logger import logger
from settings import EL, LAST_FILMWORK_KEY


@coroutine
def save_movies(state: State) -> Generator[list[Movie], None, None]:
    """Функция для сохрания данных в Elastic"""
    es = Elasticsearch(f'http://{EL["host"]}:{EL["port"]}/')
    if not es.indices.exists(index='movies'):
        es.indices.create(index='movies', body=request_body)
    es.indices.get(index='movies')
    while movies := (yield):
        logger.info(f'Received for saving {len(movies)} movies')
        data = [
            {
                '_index': 'movies',
                '_id': film_work.id,
                '_source': film_work.json(exclude={'modified'})
            }
            for film_work in movies
        ]
        try:
            bulk(es, data, index='movies')
            state.set_state(LAST_FILMWORK_KEY, str(movies[-1].modified))
            logger.info(f'Save {len(movies)} movies')
        except BulkIndexError as e:
            for error in e.errors:
                logger.info(f"Failed to index document: {error['index']['_id']}. Reason: {error['index']['error']}")
