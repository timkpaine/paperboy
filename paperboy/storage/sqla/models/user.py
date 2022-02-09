from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base


class UserSQL(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    password = Column(String)

    notebooks = relationship("NotebookSQL", back_populates="user")
    jobs = relationship("JobSQL", back_populates="user")
    reports = relationship("ReportSQL", back_populates="user")

    def __repr__(self):
        return "<User(name='%s')>" % self.name
