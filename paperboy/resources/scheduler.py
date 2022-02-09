import json
from .base import BaseResource


class SchedulerResource(BaseResource):
    def __init__(self, *args, **kwargs):
        super(SchedulerResource, self).__init__(*args, **kwargs)

    def on_get(self, req, resp):
        """Get scheduler status of job and reports"""
        resp.content_type = "application/json"
        resp.body = json.dumps(
            self.scheduler.status(req.context["user"], req.params, self.session)
        )
