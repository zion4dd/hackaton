import uvicorn
from fastapi import FastAPI
from sqlalchemy import select

from database import session_
from models import Data

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/data/")
def read_item(q: int | None = None):
    stmt = select(Data).order_by(Data.id.desc()).limit(q)
    with session_() as session:
        res = session.execute(stmt)
        res = res.scalars().all()
        print(res)

    return res


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
