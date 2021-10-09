from sqlalchemy import Table, Column, Integer, String, DateTime
from flask_security import UserMixin
from .database import Base

class User(UserMixin, Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(String)
    created_at = Column(DateTime())
    __table_args__ = {'extend_existing': True}

    def __init__(self, email, password, created_at):
        self.email = email
        self.password = password
        self.created_at = created_at

    def __repr__(self):
        return "<User('%s','%s','%s')>" % (self.email, self.password, self.created_at)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id


