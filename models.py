from typing import Annotated

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from database import engine

intpk = Annotated[int, mapped_column(primary_key=True)]


class Base(DeclarativeBase):
    pass


class Data(Base):
    __tablename__ = "data"

    id: Mapped[intpk]
    frame_number: Mapped[int]
    person_count: Mapped[int]
    heap: Mapped[int]
    frame_url: Mapped[str]
    datetime: Mapped[int]


def drop_all():
    Base.metadata.drop_all(bind=engine)


def create_all():
    Base.metadata.create_all(bind=engine)


# drop_all()
# create_all()
