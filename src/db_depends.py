from collections.abc import Generator

from sqlalchemy.orm import Session
from src.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    Зависимость для получения сессии БД. Создает новую сессию для каждого запроса и закрывает её после обработки
    """
    db: Session = SessionLocal()  # фабрика сессий

    try:  # try-finally гарантирует закрытие сесси после выполнения запроса, даже если произойдёт ошибка
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


# Generator - означает, что генератор yieldит сессию, ничего внутрь не принимает и ничего не возвращает


from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession
from src.database import async_session_maker


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

# __aexit__ объекта сессии выполняет все необходимые действия по очистке, такие как закрытие сессии или возврат соединения в пул