movies = '''
SELECT
    fw.id,
    fw.title,
    fw.description,
    fw.rating,
    fw.type,
    fw.created,
    fw.modified,
    array_to_string(
        array_remove(
            array_agg(DISTINCT p_d.full_name), null
        ), ', '
    ) as director,
    array_remove(
        array_agg(DISTINCT p_a.full_name), null
    ) as actors_names,
    array_remove(
        array_agg(DISTINCT p_w.full_name), null
    ) as writers_names,
    COALESCE (
        json_agg(
            DISTINCT jsonb_build_object(
                'id', p_a.id,
                'name', p_a.full_name
            )
        ) FILTER (WHERE p_a.id is not null),
        '[]'
    ) as actors,
    COALESCE (
        json_agg(
            DISTINCT jsonb_build_object(
                'id', p_w.id,
                'name', p_w.full_name
            )
        ) FILTER (WHERE p_w.id is not null),
        '[]'
    ) as writers,
    array_agg(DISTINCT g.name) as genre
    FROM content.film_work fw
    LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
    LEFT JOIN content.person p_d ON p_d.id = pfw.person_id and pfw.role = 'director'
    LEFT JOIN content.person p_w ON p_w.id = pfw.person_id and pfw.role = 'writer'
    LEFT JOIN content.person p_a ON p_a.id = pfw.person_id and pfw.role = 'actor'
    LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
    LEFT JOIN content.genre g ON g.id = gfw.genre_id
    WHERE fw.modified > %s
    GROUP BY fw.id
    ORDER BY fw.modified
'''


genres = '''
SELECT
    id,
    name,
    description,
    modified
FROM content.genre
WHERE modified > %s
'''

persons = '''
SELECT
    n1.id,
    n1.full_name,
    n1.modified,
    array_agg(
           DISTINCT
           jsonb_build_object(
               'uuid', film_work_id,
               'roles', roles
           )
    ) as films
FROM (
    SELECT
        p.id,
        p.full_name,
        p.modified,
        pfw.film_work_id,
        array_agg(DISTINCT pfw.role) as roles
    FROM content.person p
    LEFT JOIN content.person_film_work pfw ON pfw.person_id = p.id
    GROUP BY p.id, pfw.film_work_id
    ORDER BY p.id
) n1
WHERE n1.modified > %s
group by n1.id, n1.full_name, n1.modified
'''
