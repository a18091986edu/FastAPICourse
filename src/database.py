# # Engine - центральный компонент SQLAlchemy, который управляет подключение к БД, обеспечивает
# # - пул подключений, сохраняя открытые соединения, чтобы избежать затрат на их повторное создание, повышая производительность
# # - диалект - определяет правила взаимодействия с конкретной БД
# # - DBAPI - интерфейс взаимодействия с БД (sqlite3, psycopg2)

# from sqlalchemy import create_engine

# DATABASE_URL = "sqlite:///ecommerce.db"

# engine = create_engine(DATABASE_URL, echo=True)

# # Session (Сеанс) - объект, который управляет операциями с БД. Реализует шаблон Unit of Work, который гарантирует согласованность данных
# # - отслеживает изменения в объектах
# # - проверяет, что изменения допустимы
# # - координирует выполнение операций черех объект Engine
# # - поддерживает атомарность транзакций, что означает, что операции, выполняемые в рамках одной транзакции либо полностью применяются (commit) либо полностью отменяются (rollback)

# # Sessionmaker - фабрика сеансов, создающая экземпляры сеансов, привязанные к нашему Engine, что позволяет эффективно упрвлять подключениями, используя пул соединений из Engine


# from sqlalchemy.orm import sessionmaker, DeclarativeBase #noqa

# SessionLocal = sessionmaker(bind=engine) 
# #autocommite - убдет ли сессия автоматически фиксировать изменения в БД
# #expire_on_commit - в асинхронной сессии - параметр, который указывает SQLA следует ли сбрасывать (expire) состояние объектов в сессии после фиксации транзакции, т.е. помечать атрибуты данного объекта как устаревшие и обновлять их из БД при следующем к ним обращении. 


# class Base(DeclarativeBase):
#     pass

from sqlalchemy.orm import sessionmaker  # noqa
from sqlalchemy import create_engine

# ---------Асинхронное подключение к PostgreSQL ------
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import (create_async_engine, 
                                    async_sessionmaker,
                                    AsyncSession)

DATABASE_URL = "postgresql+asyncpg://ecommerce_user:jasmin@192.168.2.177:5433/ecommerce_db"

async_engine = create_async_engine(DATABASE_URL, echo=True)
engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(bind=engine)
async_session_maker = async_sessionmaker(async_engine,
                                         expire_on_commit=False,
                                         class_=AsyncSession)

class Base(DeclarativeBase):
    pass