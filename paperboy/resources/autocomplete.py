import json
from .base import BaseResource


class AutocompleteResource(BaseResource):
    """Autocompletion Falcon resource"""

    def __init__(self, *args, **kwargs):
        super(AutocompleteResource, self).__init__(*args, **kwargs)

    def on_get(self, req, resp):
        """Get autocompletion.

        This method calls the .search() method on the storage managers users/notebooks/jobs/reports attribute
        """
        resp.content_type = "application/json"

        params = {}
        params["name"] = req.params.get("partial", None)
        params["count"] = 10
        user = req.context["user"]

        type = req.params.get("type", None)

        if type is None:
            resp.body = json.dumps(
                self.db.notebooks.search(user, params, session=self.session)
                + self.db.jobs.search(user, params, session=self.session)
                + self.db.reports.search(user, params, session=self.session)
            )

        elif type == "notebooks":
            resp.body = json.dumps(
                self.db.notebooks.search(user, params, session=self.session)
            )
        elif type == "jobs":
            resp.body = json.dumps(
                self.db.jobs.search(user, params, session=self.session)
            )
        elif type == "reports":
            resp.body = json.dumps(
                self.db.reports.search(user, params, session=self.session)
            )
        else:
            resp.body = "No results for type {}".format(type)
