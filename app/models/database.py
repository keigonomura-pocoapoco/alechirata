from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from ..config.config import CONNECT_STR

engine = create_engine('postgresql://ejvchrmncdntmt:a46905a0329423170a3da2c4e937f57f1590ac3cfcff3d8daed25278606e64b5@ec2-54-145-188-92.compute-1.amazonaws.com:5432/d634oto7gkjca', echo=False)
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


