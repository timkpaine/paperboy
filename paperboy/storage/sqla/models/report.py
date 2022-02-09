from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from paperboy.config import ReportConfig, ReportMetadataConfig
from .base import Base


class ReportSQL(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True)
    name = Column(String)

    userId = Column(Integer, ForeignKey("users.id"))
    user = relationship("UserSQL", back_populates="reports")

    notebookId = Column(Integer, ForeignKey("notebooks.id", ondelete="cascade"))
    notebook = relationship("NotebookSQL", back_populates="reports")

    jobId = Column(Integer, ForeignKey("jobs.id", ondelete="cascade"))
    job = relationship("JobSQL", back_populates="reports")

    parameters = Column(String)
    type = Column(String)
    output = Column(String)
    strip_code = Column(Boolean)

    created = Column(DateTime)
    modified = Column(DateTime)

    @staticmethod
    def from_config(rp):
        # FIXME
        return ReportSQL(
            name=rp.name,
            userId=int(rp.user.id),
            # user=rp.user,
            notebookId=int(rp.notebook.id),
            # notebook=rp.notebook,
            jobId=int(rp.job.id),
            # job=rp.job,
            parameters=rp.meta.parameters,
            type=rp.meta.type,
            output=rp.meta.output,
            strip_code=rp.meta.strip_code,
            created=rp.meta.created,
            modified=rp.meta.modified,
        )

    def to_config(self, config):
        ret = ReportConfig(config)
        ret.id = "Report-" + str(self.id)
        ret.name = self.name

        meta = ReportMetadataConfig()
        meta.notebook = self.notebook.to_config(config)
        meta.job = self.job.to_config(config)
        meta.username = self.user.name
        meta.userid = "User-" + str(self.user.id)

        meta.parameters = self.parameters
        meta.type = self.type
        meta.output = self.output
        meta.strip_code = self.strip_code

        # meta.template = self.template  # FIXME implement
        meta.created = self.created
        meta.modified = self.modified
        ret.meta = meta
        return ret

    def __repr__(self):
        return "<Report(name='%s')>" % (self.name)
