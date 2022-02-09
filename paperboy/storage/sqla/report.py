import os
import json
import logging
from datetime import datetime
from paperboy.config import ReportConfig
from paperboy.storage import ReportStorage
from .base import BaseSQLStorageMixin, justid
from .models.user import UserSQL
from .models.notebook import NotebookSQL
from .models.job import JobSQL
from .models.report import ReportSQL


class ReportSQLStorage(BaseSQLStorageMixin, ReportStorage):
    def status(self, user, params, session, *args, **kwargs):
        base = session.query(ReportSQL).filter(ReportSQL.userId == int(user.id))

        return {
            "total": base.count(),
            "notebook": base.filter(ReportSQL.output == "notebook").count(),
            "pdf": base.filter(ReportSQL.output == "pdf").count(),
            "html": base.filter(ReportSQL.output == "html").count(),
            "email": base.filter(ReportSQL.output == "email").count(),
            "script": base.filter(ReportSQL.output == "script").count(),
        }

    def form(self):
        """Pass through to shared method in BaseSQLStorageMixin"""
        return self._form(ReportConfig)

    def search(self, user, params, session, *args, **kwargs):
        """Pass through to shared method in BaseSQLStorageMixin"""
        return self._search(ReportSQL, "Report", user, params, session, *args, **kwargs)

    def list(self, user, params, session, *args, **kwargs):
        """Pass through to shared method in BaseSQLStorageMixin"""
        return self._list(ReportSQL, "reports", user, params, session, *args, **kwargs)

    def detail(self, user, params, session, *args, **kwargs):
        """Pass through to shared method in BaseSQLStorageMixin"""
        return self._detail(ReportSQL, user, params, session, *args, **kwargs)

    def store(self, user, params, session, *args, **kwargs):
        name = params.get("name")
        user_sql = session.query(UserSQL).get(int(user.id))

        notebookid = params.get("notebook")
        nb_sql = session.query(NotebookSQL).get(int(justid(notebookid)))

        jobid = params.get("job")
        jb_sql = session.query(JobSQL).get(int(justid(jobid)))

        type = params.get("type") or "run"
        output = params.get("output") or "pdf"
        strip_code = params.get("strip_code") == "yes"
        parameters = params.get("parameters") or "[]"

        created = datetime.now()
        modified = datetime.now()

        id = params.get("id")
        if id:
            id = justid(id)
            rp = session.query(ReportSQL).filter(ReportSQL.id == id).first()
            rp.name = name
            rp.type = type
            rp.output = output
            rp.strip_code = strip_code
            rp.parameters = parameters
            rp.modified = modified

        else:
            rp = ReportSQL(
                name=name,
                userId=user.id,
                user=user_sql,
                notebookId=notebookid,
                notebook=nb_sql,
                jobId=jobid,
                job=jb_sql,
                type=type,
                output=output,
                strip_code=strip_code,
                parameters=parameters,
                created=created,
                modified=modified,
            )

        session.add(rp)

        # generate id
        session.flush()
        session.refresh(rp)

        store = rp.to_config(self.config).store()
        logging.critical("Storing report {}".format(rp))
        return store

    def generate(self, user, params, session, *args, **kwargs):
        autogen = params.get("autogen") or False
        ret = []

        if autogen:
            parameters_inline = params.get("parameters_inline") or ""
            parameters = params.get("parameters")

            if not parameters_inline and parameters:
                report_params = parameters.file.read().decode("utf-8")
            else:
                report_params = parameters_inline
            if not report_params:
                report_params = []
            else:
                report_params = [json.loads(p) for p in report_params.split(os.linesep)]

            user_sql = session.query(UserSQL).get(int(user.id))

            notebook = params.get("notebook")
            nb_sql = session.query(NotebookSQL).get(int(justid(notebook)))

            job_name = params.get("name")
            job = kwargs.get("job")
            job_id = int(justid(job.id))
            jb_sql = session.query(JobSQL).get(int(justid(job_id)))

            type = params.get("type") or "run"
            output = params.get("output") or "notebook"
            strip_code = params.get("strip_code") == "yes"

            created = datetime.now()
            modified = datetime.now()

            for i, param in enumerate(report_params):
                name = job_name + "-Report-" + str(i)
                param = json.dumps(param)
                rp = ReportSQL(
                    name=name,
                    userId=user.id,
                    user=user_sql,
                    notebookId=notebook,
                    notebook=nb_sql,
                    jobId=job_id,
                    job=jb_sql,
                    type=type,
                    output=output,
                    strip_code=strip_code,
                    parameters=param,
                    created=created,
                    modified=modified,
                )
                session.add(rp)

                # FIXME
                session.flush()
                session.refresh(rp)
                ret.append(rp.to_config(self.config))

            session.flush()

        return ret

    def delete(self, user, params, session, *args, **kwargs):
        # TODO only if allowed
        id = justid(params.get("id"))
        rp = session.query(ReportSQL).filter(ReportSQL.id == id).first()
        name = rp.name
        session.delete(rp)
        return [
            {
                "name": "",
                "type": "p",
                "value": "Success!",
                "required": False,
                "readonly": False,
                "hidden": False,
            },
            {
                "name": "",
                "type": "p",
                "value": "Successfully deleted report: " + name,
                "required": False,
                "readonly": False,
                "hidden": False,
            },
        ]
