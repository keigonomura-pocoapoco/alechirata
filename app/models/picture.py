from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Picture(Base):
    __tablename__ = 'pictures'
    id = Column(Integer, primary_key=True)
    picture_url = Column(String)
    folder = Column(String)
    uploaded_at = Column(DateTime())
    __table_args__ = {'extend_existing': True}

    def __init__(self, picture_url, folder, uploaded_at):
        self.picture_url = picture_url
        self.folder = folder
        self.uploaded_at = uploaded_at

    def __repr__(self):
        return "<Post('%s','%s','%s')>" % (self.picture_url, self.folder, self.uploaded_at)