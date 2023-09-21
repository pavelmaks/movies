from datetime import datetime
from typing import Generator

from decorators import coroutine
from elasticsearch import Elasticsearch, helpers
from indexes import Index
from psycopg import ServerCursor
from pydantic import BaseModel
from settings import FETCH_BY, logger
from state.state import State


class BaseEtl:
    def __init__(self, curr: ServerCursor, es: Elasticsearch, state: State,
                 index: Index, query: str, table: BaseModel, state_key: str) -> None:
        self.curr = curr
        self.es = es
        self.state = state
        self.index = index
        self.query = query
        self.table = table
        self.state_key = state_key
        self.__run()

    def __call__(self) -> None:
        """Запускает ETL процесс"""
        self.extract_coro.send(self.state.get_state(self.state_key) or str(datetime.min))

    def __run(self):
        """Связывает корутины и создает индекс"""
        if not self.es.indices.exists(index=self.index.name):
            self.es.indices.create(index=self.index.name, body=self.index.schema)
        load_coro = self.load(self.state)
        transform_coro = self.transform(load_coro)
        self.extract_coro = self.extract(self.curr, transform_coro)

    @coroutine
    def extract(self, cursor, next_node: Generator) -> Generator[datetime, None, None]:
        while last_updated := (yield):
            logger.info(f'Fetching {self.table} updated after %s', last_updated)
            cursor.execute(self.query, (last_updated,))
            while results := cursor.fetchmany(size=FETCH_BY):
                next_node.send(results)

    @coroutine
    def transform(self, next_node: Generator) -> Generator[list[dict], None, None]:
        while objs_dicts := (yield):
            batch = []
            for obj in objs_dicts:
                obj = self.table(**obj)
                logger.info(obj.json())
                batch.append(obj)
            next_node.send(batch)

    @coroutine
    def load(self, state: State) -> Generator[list[BaseModel], None, None]:
        objs_list: list[BaseModel]
        while objs_list := (yield):
            logger.info(f'Received for saving {len(objs_list)} {self.table}')

            actions = [
                {
                    '_id': obj.id,
                    '_source': obj.dict(exclude={'modified'})
                }
                for obj in objs_list
            ]
            helpers.bulk(self.es, actions, index=self.index.name)

            state.set_state(self.state_key, str(objs_list[-1].modified))
