from sqlalchemy import create_engine, text
from typing import Iterable, Dict
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///db.sqlite", echo=True, connect_args={'check_same_thread': False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Database:
    def __init__(self):
        self._engine = create_engine(**self._connection_arguments)

    @property
    def _connection_arguments(self):
        return {
            'url': "sqlite:///db.sqlite",
            'echo': True,
            'connect_args': {
                'check_same_thread': False
            }
        }

    @property
    def _session_arguments(self):
        return {
            'autocommit': False,
            'autoflush': False,
            'bind': self._engine
        }
    
    @property
    def session(self):
        session = sessionmaker(**self._session_arguments, expire_on_commit=False)
        return session()

    def __enter__(self):
        return self.session

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.close()
        
async def get_db():
    with Database() as db:
        db.execute(text("PRAGMA foreign_keys = ON;"))
        yield db
