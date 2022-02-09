from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models.base import Base
from .models.user import UserSQL
from .models.notebook import NotebookSQL
from .models.job import JobSQL
from .models.report import ReportSQL


def main(sql_url):
    """Create dummy notebook data for sqlalchemy"""
    engine = create_engine(sql_url, echo=False)
    Base.metadata.create_all(engine)
    sm = sessionmaker(bind=engine)

    session = sm()
    user = UserSQL(name="test")
    session.add(user)
    session.commit()
    session.refresh(user)

    notebook = """
    """
    created = datetime.now()
    modified = datetime.now()

    notebook = NotebookSQL(
        name="MyNotebook",
        userId=user.id,
        user=user,
        notebook="",
        privacy="",
        level="",
        requirements="",
        dockerfile="",
        created=created,
        modified=modified,
    )
    session.add(notebook)
    session.commit()
    session.refresh(notebook)

    job = JobSQL(
        name="MyJob",
        userId=user.id,
        user=user,
        notebookId=notebook.id,
        notebook=notebook,
        start_time=created,
        interval="minutely",
        level="production",
        created=created,
        modified=modified,
    )
    session.add(job)
    session.commit()
    session.refresh(job)

    type = "run"
    output = "notebook"
    strip_code = True

    created = datetime.now()
    modified = datetime.now()

    name = job.name + "-Report-1"

    param = "{}"
    report = ReportSQL(
        name=name,
        userId=user.id,
        user=user,
        notebookId=notebook.id,
        notebook=notebook,
        jobId=job.id,
        job=job,
        type=type,
        output=output,
        strip_code=strip_code,
        parameters=param,
        created=created,
        modified=modified,
    )
    session.add(report)
    session.commit()
    session.refresh(report)
