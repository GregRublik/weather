from sqlalchemy import create_engine, insert, select, update
from db.config import settings
from db.models import cities, users_history, users
import ast


engine = create_engine(
    url=settings.database_url_psycopg,
    pool_size=5,
    max_overflow=10
)


def select_cities_name() -> list[str]:
    with engine.connect() as conn:
        result = conn.execute(
            select(cities.c.name)
        )
        conn.commit()
        list_cities: list[str] = []
        for i in result.all():
            list_cities.append(i[0])
        return list_cities


def insert_history(username: str) -> None:
    with engine.connect() as conn:

        result = conn.execute(
            insert(users).values(username=username)
        )
        conn.commit()


def insert_into(city: str):
    with engine.connect() as conn:
        city = city.capitalize()
        city_match = conn.execute(select(cities).where(cities.c.name == city)).fetchone()
        if city_match:
            conn.execute(
                update(cities).
                where(cities.c.name == city).
                values(count_requests=cities.c.count_requests + 1)
            )
        else:
            conn.execute(
                insert(cities).
                values(name=city,count_requests=cities.c.count_requests + 1)
            )
        conn.commit()
        return city_match[0]


def get_history() -> list:
    with engine.connect() as conn:
        statistics = conn.execute(select(cities))
        conn.commit()
        all_info = []
        info = {}
        for i in statistics:
            info['id'] = i[0]
            info["name"] = i[1]
            info['count'] = i[2]
            all_info.append(info)
    return all_info


def del_history():
    with engine.connect() as conn:
        conn.execute(update(cities).values(count_requests=0))
        conn.commit()


def new_history_user(user: str, city: str):
    with engine.connect() as conn:
        conn.execute(insert(users_history).values(user=user, city=city))
        conn.commit()


def new_user(username: str):
    with engine.connect() as conn:
        conn.execute(insert(users).values(username=username))
        conn.commit()


def get_user(username: str):
    with engine.connect() as conn:
        res = conn.execute(select(users).where(users.c.username == username))
        conn.commit()
        return res.all()


def get_history_user(user) -> list:
    with engine.connect() as conn:
        res = conn.execute(select(cities.c.name).select_from(
        users_history.join(cities, users_history.c.city == cities.c.id)).where(users_history.c.user == user))

        conn.commit()
        list_history = []
        for i in res:
            list_history.append(i[0])

    return list_history


def fill_city():
    with engine.connect() as conn:
        cities_list = []
        with open('db/list_cities.txt', "r", encoding='utf-8') as file:
            list_city = file.read()
            city = ast.literal_eval(list_city)
            for i in city:
                cities_list.append({"name": i, "count_requests": 0})

        conn.execute(
            insert(cities).values(cities_list)
            )
        conn.commit()