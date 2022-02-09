import json
from .base import BaseResource


class JobResource(BaseResource):
    def __init__(self, *args, **kwargs):
        super(JobResource, self).__init__(*args, **kwargs)

    def on_get(self, req, resp):
        """List all job instances"""
        resp.content_type = "application/json"
        resp.body = json.dumps(
            self.db.jobs.list(req.context["user"], req.params, self.session)
        )

    def on_post(self, req, resp):
        """Create new or delete job instance"""
        resp.content_type = "application/json"
        action = req.params.get("action")
        if action == "delete":
            resp.body = json.dumps(
                self.db.jobs.delete(
                    req.context["user"], req.params, self.session, self.scheduler
                )
            )
        else:
            resp.body = json.dumps(
                self.db.jobs.store(
                    req.context["user"], req.params, self.session, self.scheduler
                )
            )


class JobDetailResource(BaseResource):
    def __init__(self, *args, **kwargs):
        super(JobDetailResource, self).__init__(*args, **kwargs)

    def on_get(self, req, resp):
        """Get details of specific job instance"""
        resp.content_type = "application/json"
        resp.body = json.dumps(
            self.db.jobs.detail(req.context["user"], req.params, self.session)
        )
