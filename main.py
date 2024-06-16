import uvicorn
from fastapi import FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select

from config import settings
from database import session_
from models import Data, FireBase


def create_fastapi():
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
    )

    @app.get("/")
    def read_root():
        return {"Hello": "World"}

    @app.get("/data/")
    def read_item(q: int | None = None, x_firebase_token: str | None = Header(None)):
        if x_firebase_token:
            print(f"{x_firebase_token=}")
            stmt = select(FireBase).where(FireBase.name == settings.FBConsumer)
            with session_() as session:
                res = session.execute(stmt).scalars().first()
                if not res:
                    res = FireBase(name=settings.FBConsumer)
                    session.add(res)
                if res.token != x_firebase_token:
                    res.token = x_firebase_token
                    session.commit()

        stmt = select(Data).order_by(Data.id.desc()).limit(q)
        with session_() as session:
            res = session.execute(stmt)
            res = res.scalars().all()
            print("return:", len(res))

        return res

    return app


app = create_fastapi()

if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
