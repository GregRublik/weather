from sqlalchemy import Table, Column, Integer, String, ForeignKey, MetaData
from sqlalchemy.orm import declarative_base


Base = declarative_base()
metadata_obj = MetaData()


users = Table(
    "users",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("username", String(125)),
)

users_history = Table(
    "users_history",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user", Integer, ForeignKey("users.id")),
    Column("city", Integer, ForeignKey("cities.id")),
)

cities = Table(
    "cities",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name",String(30), nullable=False),
    Column("count_requests", Integer),
)
