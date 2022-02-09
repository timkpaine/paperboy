import falcon
import jinja2
from .base import BaseResource
from .html import read


class LogoutResource(BaseResource):
    """Falcon resource for user authentication"""

    auth_required = False

    def __init__(self, *args, **kwargs):
        super(LogoutResource, self).__init__(*args, **kwargs)

    def on_get(self, req, resp):
        """Get logout page"""
        resp.content_type = "text/html"
        file = read("logout.html")
        tpl = jinja2.Template(file).render(
            baseurl=self.config.baseurl,
            apiurl=self.config.apiurl,
            loginurl=self.config.loginurl,
            logouturl=self.config.logouturl,
        )
        resp.body = tpl

    def on_post(self, req, resp):
        """Log user out using authentication backend"""
        ret = self.db.users.logout(req.context.get("user"), req.params, self.session)

        if req.context.get("user"):
            # remove user from context
            req.context["user"] = None

        if req.context.get("auth_token"):
            # remove auth token from context
            req.context["auth_token"] = None

        if ret:
            # delete cookie and refresh page to base
            resp.unset_cookie("auth_token")
            resp.status = falcon.HTTP_302
            resp.set_header("Location", self.config.baseurl)
