import json
from .base import BaseResource


class StatusResource(BaseResource):
    def __init__(self, *args, **kwargs):
        super(StatusResource, self).__init__(*args, **kwargs)

    def on_get(self, req, resp):
        """get status report for notebooks/jobs/reports or all"""
        type = req.params.get("type", "")
        if type == "notebooks":
            resp.body = json.dumps(
                self.db.notebooks.status(req.context["user"], req.params, self.session)
            )
        elif type == "jobs":
            resp.body = json.dumps(
                self.db.jobs.status(req.context["user"], req.params, self.session)
            )
        elif type == "reports":
            resp.body = json.dumps(
                self.db.reports.status(req.context["user"], req.params, self.session)
            )
        else:
            ret = {}
            ret["notebooks"] = self.db.notebooks.status(
                req.context["user"], req.params, self.session
            )
            ret["jobs"] = self.db.jobs.status(
                req.context["user"], req.params, self.session
            )
            ret["reports"] = self.db.reports.status(
                req.context["user"], req.params, self.session
            )
            resp.body = json.dumps(ret)
