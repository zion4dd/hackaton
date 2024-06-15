from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker  # DeclarativeBase, Session

from config import settings

engine = create_engine(
    settings.DB_URL_psycopg,
    echo=False,
    # pool_size=5,
    # max_overflow=10,
)

session_ = sessionmaker(bind=engine)
