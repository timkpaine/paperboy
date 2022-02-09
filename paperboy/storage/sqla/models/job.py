from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from paperboy.config import JobConfig, JobMetadataConfig
from .base import Base


class JobSQL(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True)
    name = Column(String)

    userId = Column(Integer, ForeignKey("users.id"))
    user = relationship("UserSQL", back_populates="jobs")

    notebookId = Column(Integer, ForeignKey("notebooks.id", ondelete="cascade"))
    notebook = relationship("NotebookSQL", back_populates="jobs")

    reports = relationship(
        "ReportSQL", cascade="all,delete,delete-orphan", back_populates="job"
    )

    start_time = Column(DateTime)
    interval = Column(String)
    level = Column(String, nullable=True)

    created = Column(DateTime)
    modified = Column(DateTime)

    @staticmethod
    def from_config(jb):
        # FIXME
        return JobSQL(
            name=jb.name,
            userId=int(jb.user.id),
            # user=jb.user,
            notebookId=int(jb.notebook.id),
            # notebook=jb.notebook,
            reports=jb.meta.reports,
            start_time=jb.meta.start_time,
            interval=jb.meta.interval,
            level=jb.meta.level,
            created=jb.meta.created,
            modified=jb.meta.modified,
        )

    def to_config(self, config):
        ret = JobConfig(config)
        ret.id = "Job-" + str(self.id)
        ret.name = self.name

        meta = JobMetadataConfig()
        meta.notebook = self.notebook.to_config(config)
        meta.username = self.user.name
        meta.userid = "User-" + str(self.user.id)

        meta.start_time = self.start_time
        meta.interval = self.interval
        meta.level = self.level

        meta.reports = len(self.reports)

        meta.created = self.created
        meta.modified = self.modified

        ret.meta = meta
        return ret

    def __repr__(self):
        return "<Job(name='{}', user='{}', notebook='{}', start='{}', interval='{}'>".format(
            self.name, self.user, self.notebook, self.start_time, self.interval
        )
