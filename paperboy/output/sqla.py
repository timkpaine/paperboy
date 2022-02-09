from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from paperboy.storage.sqla.models.output import OutputSQL
from .base import BaseOutput


class SQLAOutput(BaseOutput):
    """Output to sql database"""

    def __init__(self, config, *args, **kwargs):
        self.config = config
        self.engine = create_engine(self.storage.sql_url, echo=False)
        self.sessionmaker = sessionmaker(bind=self.engine)

    def write(self, report, output, *args, **kwargs):
        task_id = kwargs.get("task_id", "")
        name = task_id + "_" + datetime.now().strftime("%m-%d-%Y_%H-%M-%S")

        if report["meta"]["output"] == "notebook":
            name += ".ipynb"
        elif report["meta"]["output"] == "script":
            name += ".py"
        elif report["meta"]["output"] == "email":
            name += ".eml"
        elif report["meta"]["output"] in ("pdf", "html"):
            name += ".{}".format(report["meta"]["output"])

        with self.sessionmaker() as session:
            report_id = int(report["id"])
            created = datetime.now()

            out = OutputSQL(name=name, reportId=report_id, created=created)
            session.add(out)
            session.flush()
