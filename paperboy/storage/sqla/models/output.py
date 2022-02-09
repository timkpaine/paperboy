from sqlalchemy import Column, Integer, String, DateTime, LargeBinary
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class OutputSQL(Base):
    __tablename__ = "outputs"
    id = Column(Integer, primary_key=True)
    name = Column(String)

    reportId = Column(Integer, ForeignKey("reports.id"))
    report = relationship("ReportSQL", back_populates="outputs")

    created = Column(DateTime)
    data = LargeBinary()

    def __repr__(self):
        return "<Output(name='%s')>" % (self.name)
