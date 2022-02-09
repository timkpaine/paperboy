import json
from .base import BaseResource


class NotebookResource(BaseResource):
    def __init__(self, *args, **kwargs):
        super(NotebookResource, self).__init__(*args, **kwargs)

    def on_get(self, req, resp):
        """List all notebook instances"""
        resp.content_type = "application/json"
        resp.body = json.dumps(
            self.db.notebooks.list(req.context["user"], req.params, self.session)
        )

    def on_post(self, req, resp):
        """Create new or delete old notebook instance"""
        resp.content_type = "application/json"
        action = req.params.get("action")
        if action == "delete":
            resp.body = json.dumps(
                self.db.notebooks.delete(req.context["user"], req.params, self.session)
            )
        else:
            resp.body = json.dumps(
                self.db.notebooks.store(req.context["user"], req.params, self.session)
            )


class NotebookDetailResource(BaseResource):
    def __init__(self, *args, **kwargs):
        super(NotebookDetailResource, self).__init__(*args, **kwargs)

    def on_get(self, req, resp):
        """Get details of specific notebook instance"""
        resp.content_type = "application/json"
        resp.body = json.dumps(
            self.db.notebooks.detail(req.context["user"], req.params, self.session)
        )
