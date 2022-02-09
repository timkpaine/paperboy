import falcon
import uuid


class StorageEngine(object):
    """Unified interface into storage classes of a backend"""

    ################################
    # These attributes must be set #
    users = property(lambda self: self._user_storage)
    notebooks = property(lambda self: self._notebook_storage)
    jobs = property(lambda self: self._job_storage)
    reports = property(lambda self: self._report_storage)
    ################################

    def __init__(self, user_storage, notebook_storage, job_storage, report_storage):
        # resources get with self.db
        self._user_storage = user_storage
        self._notebook_storage = notebook_storage
        self._job_storage = job_storage
        self._report_storage = report_storage

        # storage classes get with self.db
        self._user_storage.db = self
        self._notebook_storage.db = self
        self._job_storage.db = self
        self._report_storage.db = self

    def get_things(self, marker, limit):
        return [{"id": str(uuid.uuid4()), "color": "green"}]

    def add_thing(self, thing):
        thing["id"] = str(uuid.uuid4())
        return thing


class StorageError(Exception):
    @staticmethod
    def handle(ex, req, resp, params):
        description = (
            "Sorry, couldn't write your thing to the " "database. It worked on my box."
        )

        raise falcon.HTTPError(falcon.HTTP_725, "Database Error", description)
