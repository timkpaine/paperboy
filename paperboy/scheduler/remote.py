import requests
from .base import BaseScheduler


class RemoteScheduler(BaseScheduler):
    """Proxy methods to a remote worker instance"""

    def __init__(self, *args, **kwargs):
        super(RemoteScheduler, self).__init__(*args, **kwargs)

    def status(self, user, params, session, *args, **kwargs):
        # FIXME async/celery
        return requests.get(self.config.scheduler.status_url, params=params).json()

    def schedule(self, user, notebook, job, reports, *args, **kwargs):
        # FIXME async/celery
        params = {
            "user": user.to_json(),
            "notebook": notebook.to_json(),
            "job": job.to_json(),
            "reports": [r.to_json() for r in reports],
        }
        return requests.post(self.config.scheduler.schedule_url, params=params).json()

    def unschedule(self, user, notebook, job, reports, *args, **kwargs):
        return self.schedule(user, notebook, job, reports, *args, **kwargs)
