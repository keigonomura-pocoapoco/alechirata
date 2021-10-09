from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Folder(Base):
    __tablename__ = 'folders'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    created_at = Column(DateTime())
    __table_args__ = {'extend_existing': True}

    def __init__(self, name, created_at):
        self.name = name
        self.created_at = created_at

    def __repr__(self):
        return "<Post('%s','%s')>" % (self.name, self.created_at)