from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from ..config.config import CONNECT_STR

engine = create_engine('postgresql://alechirata:KeigoUWC0126!@alec-flask11.ceovgizni3bq.ap-northeast-1.rds.amazonaws.com:5432/alc', echo=False)
session = scoped_session(
            sessionmaker(
                autocommit = False,
                autoflush = True,
                bind = engine))

Base = declarative_base()
Base.query = session.query_property()

def init_db():
    import app.models
    Base.metadata.create_all(bind=engine)


