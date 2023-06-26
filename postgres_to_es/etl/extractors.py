from datetime import datetime
from typing import Generator, Any

from psycopg import ServerCursor

from decorators import coroutine
from logger import logger


@coroutine
def fetch_changed_movies(cursor: ServerCursor, next_node: Generator) -> Generator[dict[str, Any], None, None]:
    """Генератор для выгрузки данных о измененных фильмах"""
    while fw_ids := (yield):
        logger.info(f'Fetching movies changed after ' f'{fw_ids}')
        fw_ids = [str(fw['id']) for fw in fw_ids]
        sql = """
            SELECT
                fw.id as id,
                fw.title,
                fw.description,
                fw.rating,
                fw.modified,
                COALESCE (
                    ARRAY_AGG(
                        DISTINCT g.name
                    ),
                    '{}'
                ) AS genre,
                string_agg(DISTINCT CASE WHEN pfw.role = 'director' THEN p.full_name ELSE '' END, ',') AS director,
                array_remove(
                    COALESCE(array_agg(
                        DISTINCT CASE WHEN pfw.role = 'actor' THEN p.full_name END)
                        FILTER (WHERE p.full_name IS NOT NULL)), NULL
                ) AS actors_names,
                array_remove(
                    COALESCE(array_agg(
                        DISTINCT CASE WHEN pfw.role = 'writer' THEN p.full_name END)
                        FILTER (WHERE p.full_name IS NOT NULL)), NULL
                ) AS writers_names,
                COALESCE (
                    JSON_AGG(
                        DISTINCT JSONB_BUILD_OBJECT(
                            'id', p.id,
                            'name', p.full_name
                        )
                    ) FILTER (WHERE pfw.role = 'actor'),
                    '[]'
                ) as actors,
                COALESCE (
                JSON_AGG(
                    DISTINCT JSONB_BUILD_OBJECT(
                        'id', p.id,
                        'name', p.full_name
                    )
                ) FILTER (WHERE pfw.role = 'writer'),
                '[]'
            ) as writers
            FROM content.film_work as fw
            LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
            LEFT JOIN content.person p ON p.id = pfw.person_id
            LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
            LEFT JOIN content.genre g ON g.id = gfw.genre_id
            WHERE fw.id = ANY(%s)
            GROUP BY fw.id
            ORDER BY fw.modified;
            LIMIT 100;
        """
        cursor.execute(sql, [fw_ids])
        while results := cursor.fetchmany(size=100):
            next_node.send(results)

@coroutine
def fetch_changed_filmworks(cursor, next_node: Generator) -> Generator[datetime, None, None]:
    """Генератор по ids измененных фильмов"""
    while last_updated := (yield):
        logger.info(f'Fetching filmworks changed after ' f'{last_updated}')
        sql = """
            SELECT id FROM content.film_work
            WHERE film_work.modified > %s
            order by film_work.modified asc
            LIMIT 100;
        """
        cursor.execute(sql, (last_updated,))
        while results := cursor.fetchmany(size=100):
            next_node.send(results)
