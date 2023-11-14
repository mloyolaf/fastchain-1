from fastapi import FastAPI
from api import router
from db.orm.models import Base
import db.orm

app = FastAPI()

app.include_router(router)

@app.on_event("startup")
async def setup_db():
    Base.metadata.create_all(db.orm.engine)

@app.get("/")
async def root():
    print(app.routes)
    return { "Hola": "mundo" }
