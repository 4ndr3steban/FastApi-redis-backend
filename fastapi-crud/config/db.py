from sqlalchemy import create_engine
from settings import settings
from .models import Base, Tmetric
from time import sleep

flag = False

# while not flag:
#     try:
#         # Conexión a la base de datos MySql para datos de usuarios y queries
#         engine = create_engine(f"mysql://{settings.MYSQL_USER}:{settings.MYSQL_PASS}@{settings.MYSQL_HOST}:{settings.MYSQL_PORT}/{settings.MYSQL_DB}")

#         # Metadata para crear las tablas en la db y los tipos de datos en ellas
#         Base.metadata.create_all(bind=engine)

#         flag = True
#     except Exception:
#         sleep(15)

#Conexión a la base de datos MySql para datos de usuarios y queries
engine = create_engine(f"mysql://{settings.MYSQL_USER}:{settings.MYSQL_PASS}@{settings.MYSQL_HOST}:{settings.MYSQL_PORT}/{settings.MYSQL_DB}")

# Metadata para crear las tablas en la db y los tipos de datos en ellas
Base.metadata.create_all(bind=engine)