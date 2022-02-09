from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from paperboy.config import NotebookConfig, NotebookMetadataConfig
from .base import Base


class NotebookSQL(Base):
    __tablename__ = "notebooks"
    id = Column(Integer, primary_key=True)
    name = Column(String)

    userId = Column(Integer, ForeignKey("users.id"))
    user = relationship("UserSQL", back_populates="notebooks")

    jobs = relationship(
        "JobSQL", cascade="all,delete,delete-orphan", back_populates="notebook"
    )
    reports = relationship(
        "ReportSQL", cascade="all,delete,delete-orphan", back_populates="notebook"
    )

    notebook = Column(String)
    privacy = Column(String, nullable=True)
    level = Column(String, nullable=True)
    requirements = Column(String, nullable=True)
    dockerfile = Column(String, nullable=True)

    created = Column(DateTime)
    modified = Column(DateTime)

    @staticmethod
    def from_config(nb):
        # FIXME
        return NotebookSQL(
            name=nb.name,
            userId=int(nb.user.id),
            notebook=nb.notebook,
            privacy=nb.meta.privacy,
            level=nb.meta.level,
            requirements=nb.meta.requirements,
            dockerfile=nb.meta.dockerfile,
            created=nb.meta.created,
            modified=nb.meta.modified,
        )

    def to_config(self, config):
        ret = NotebookConfig(config)
        ret.id = "Notebook-" + str(self.id)
        ret.name = self.name

        meta = NotebookMetadataConfig()

        meta.username = self.user.name
        meta.userid = "User-" + str(self.user.id)

        meta.notebook = self.notebook
        meta.privacy = self.privacy
        meta.level = self.level

        meta.requirements = self.requirements
        meta.dockerfile = self.dockerfile

        meta.jobs = len(self.jobs)
        meta.reports = len(self.reports)

        meta.created = self.created
        meta.modified = self.modified

        ret.meta = meta
        return ret

    def __repr__(self):
        return "<Notebook(name='{}', user='{}', privacy='{}', level='{}'>".format(
            self.name, self.user, self.privacy, self.level
        )
