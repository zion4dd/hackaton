from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker  # DeclarativeBase, Session

url = "postgresql+psycopg2://postgres:postgres@localhost:5432/hackaton"

engine = create_engine(
    url,
    echo=False,
    # pool_size=5,
    # max_overflow=10,
)

session_ = sessionmaker(bind=engine)
