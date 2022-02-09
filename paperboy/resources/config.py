import falcon
import json
from .base import BaseResource


class ConfigResource(BaseResource):
    """Falcon resource to get form entries"""

    def __init__(self, *args, **kwargs):
        super(ConfigResource, self).__init__(*args, **kwargs)

    def on_get(self, req, resp):
        """Get configuration page to create a new notebook/job/report"""
        resp.content_type = "application/json"
        type = req.params.get("type", None)
        if type is None:
            resp.body = json.dumps(self.config.to_dict())
        elif type == "notebooks":
            resp.body = json.dumps(self.db.notebooks.form())
        elif type == "jobs":
            resp.body = json.dumps(self.db.jobs.form())
        elif type == "reports":
            resp.body = json.dumps(self.db.reports.form())
        else:
            resp.status = falcon.HTTP_404
