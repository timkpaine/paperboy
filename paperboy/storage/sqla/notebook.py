import nbformat
import logging
from datetime import datetime
from paperboy.config import NotebookConfig
from paperboy.storage import NotebookStorage
from sqlalchemy import or_
from .base import BaseSQLStorageMixin, justid
from .models.user import UserSQL
from .models.notebook import NotebookSQL
from ..utils import strip_outputs


class NotebookSQLStorage(BaseSQLStorageMixin, NotebookStorage):
    def status(self, user, params, session, *args, **kwargs):
        base = session.query(NotebookSQL).filter(
            or_(
                NotebookSQL.userId.like((user.id)),
                (hasattr(NotebookSQL, "privacy") and NotebookSQL.privacy == "public"),
            )
        )

        return {
            "total": base.count(),
            "public": base.filter(NotebookSQL.level == "public").count(),
            "private": base.filter(NotebookSQL.privacy == "private").count(),
        }

    def form(self):
        """Pass through to shared method in BaseSQLStorageMixin"""
        return self._form(NotebookConfig)

    def search(self, user, params, session, *args, **kwargs):
        """Pass through to shared method in BaseSQLStorageMixin"""
        return self._search(
            NotebookSQL, "Notebook", user, params, session, *args, **kwargs
        )

    def list(self, user, params, session, *args, **kwargs):
        """Pass through to shared method in BaseSQLStorageMixin"""
        return self._list(
            NotebookSQL, "notebooks", user, params, session, *args, **kwargs
        )

    def detail(self, user, params, session, *args, **kwargs):
        """Pass through to shared method in BaseSQLStorageMixin"""
        return self._detail(NotebookSQL, user, params, session, *args, **kwargs)

    def store(self, user, params, session, *args, **kwargs):
        name = params.get("name")
        user_sql = session.query(UserSQL).get(int(user.id))

        if params.get("file") is not None:
            notebook = nbformat.writes(
                strip_outputs(nbformat.reads(params.get("file").file.read(), 4))
            )
        elif params.get("notebook"):
            notebook = nbformat.writes(
                strip_outputs(nbformat.reads(params.get("notebook"), 4))
            )
        else:
            raise NotImplementedError()

        privacy = params.get("privacy") or ""
        level = params.get("level") or ""

        if params.get("requirements") is not None:
            try:
                requirements = params.get("requirements").file.read()
            except AttributeError:
                requirements = ""
        else:
            requirements = ""

        if params.get("dockerfile"):
            try:
                params.get("dockerfile").file.read()
            except AttributeError:
                requirements = ""

        else:
            dockerfile = ""

        created = datetime.now()
        modified = datetime.now()

        id = params.get("id")
        if id:
            id = justid(id)
            nb = session.query(NotebookSQL).filter(NotebookSQL.id == id).first()
            nb.name = name
            nb.notebook = notebook
            nb.privacy = privacy
            nb.level = level
            nb.requirements = requirements
            nb.dockerfile = dockerfile
            nb.modified = modified

        else:
            nb = NotebookSQL(
                name=name,
                userId=int(user.id),
                user=user_sql,
                notebook=notebook,
                privacy=privacy,
                level=level,
                requirements=requirements,
                dockerfile=dockerfile,
                created=created,
                modified=modified,
            )

        session.add(nb)

        # generate id
        session.flush()
        session.refresh(nb)

        store = nb.to_config(self.config).store()
        logging.critical("Storing notebook {}".format(nb))
        return store

    def delete(self, user, params, session, *args, **kwargs):
        # TODO only if allowed
        id = justid(params.get("id"))
        nb = session.query(NotebookSQL).filter(NotebookSQL.id == id).first()
        name = nb.name
        session.delete(nb)

        # cascade handled in DB, need to cascade to airflow jobs
        from .models.job import JobSQL

        jobs = session.query(JobSQL).filter(JobSQL.notebookId == nb.id).all()
        for job in jobs:
            resp = self.db.jobs.delete(user, {"id": job.id}, session, *args, **kwargs)
            print(resp)
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
                "value": "Successfully deleted notebook: " + name,
                "required": False,
                "readonly": False,
                "hidden": False,
            },
        ]
