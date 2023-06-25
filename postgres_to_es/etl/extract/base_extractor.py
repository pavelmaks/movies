from datetime import datetime
from logger import logger
from typing import Generator
from decorators import coroutine

class BaseExtractor:
    def __init__(self) -> None:
        pass


@coroutine
def fetch_changed_movies(cursor, next_node: Generator) -> Generator[datetime, None, None]:
    while last_updated := (yield):
        logger.info(f'Fetching movies changed after ' f'{last_updated}')
        sql = 'SELECT * FROM content.film_work WHERE film_work.modified > %s order by film_work.modified asc LIMIT 100'
        logger.info('Fetching movies updated after %s', last_updated)
        cursor.execute(sql, (last_updated,))
        while results := cursor.fetchmany(size=100):
            next_node.send(results)
