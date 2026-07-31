import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from dotenv import load_dotenv

from database.orm import Base


load_dotenv()
db_url = os.getenv("DB_URL")

if db_url is None:
    raise ConnectionError("DB URL is not found! Create or edit .env file!")

psql_engine = create_engine(db_url)
Base.metadata.create_all(psql_engine)

Session = sessionmaker(psql_engine)

@contextmanager
def get_db() -> Session:
    db = Session()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()