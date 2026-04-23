from sqlalchemy.orm import Session
from collections.abc import Generator

from src.database import SessionLocal

def get_db() -> Generator[Session, None, None]:
    """
    Зависимость для получения сессии БД. Создает новую сессию для каждого запроса и закрывает её после обработки
    """
    db: Session = SessionLocal() # фабрика сессий

    try: # try-finally гарантирует закрытие сесси после выполнения запроса, даже если произойдёт ошибка
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


# Generator - означает, что генератор yieldит сессию, ничего внутрь не принимает и ничего не возвращает


