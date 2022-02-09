import falcon
import os
import os.path
import mimetypes
import jinja2

# from functools import lru_cache
from .base import BaseResource


# @lru_cache(20)
def read(file):
    """read a file from local disk"""
    path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "assets", "templates", file)
    )
    if not os.path.exists(path):
        return None
    with open(path, "r") as fp:
        return fp.read()


class HTMLResource(BaseResource):
    """Falcon resource to service HTML files templated with jinja2"""

    def __init__(self, *args, **kwargs):
        super(HTMLResource, self).__init__(*args, **kwargs)

    def on_get(self, req, resp):
        """Get templatized html and render"""
        if req.path == "" or req.path == "/":
            path = "index.html"
        else:
            path = req.path

        filetype = mimetypes.guess_type(path, strict=True)[0]
        resp.content_type = filetype

        file = read(path)
        if file:
            tpl = jinja2.Template(file).render(
                user=req.context.get("user").name,
                baseurl=self.config.baseurl,
                apiurl=self.config.apiurl,
                loginurl=self.config.loginurl,
                logouturl=self.config.logouturl,
            )
            resp.body = tpl
        else:
            resp.status = falcon.HTTP_404
