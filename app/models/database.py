from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from ..config.config import CONNECT_STR

engine = create_engine('postgresql://sdsgoubmroepjg:bea71326aeb64aa1a2675b5e2f895b7a2ef59017a29ed16ab8b4a2acf9558e43@ec2-54-161-189-150.compute-1.amazonaws.com:5432/dafcbomp5q6jqs', echo=False)
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


