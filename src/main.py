from fastapi import FastAPI
from src.api import router
from src.db.orm.models import Base
import src.db.orm
from dotenv import load_dotenv
import os

load_dotenv() 
api_key = os.getenv('OPENAI_API_KEY')
app = FastAPI()

app.include_router(router)

@app.on_event("startup")
async def setup_db():
    Base.metadata.create_all(src.db.orm.engine)

@app.get("/")
async def root():
    print(app.routes)
    return { "Hola": "mundo" }
