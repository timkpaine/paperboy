import falcon
import os
import os.path
import mimetypes

# from functools import lru_cache
from .base import BaseResource


# @lru_cache(20)
def read(file):
    """read static resource from disk (js/css/etc)"""
    path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "assets",
            "static",
            file.replace("/static/", ""),
        )
    )
    if not os.path.exists(path):
        return None
    with open(path, "rb") as fp:
        return fp.read()


class StaticResource(BaseResource):
    """Falcon resource to service CSS/JS/image/font files"""

    auth_required = False

    def __init__(self, *args, **kwargs):
        super(StaticResource, self).__init__(*args, **kwargs)

    def on_get(self, req, resp):
        """read and return resource with appropriate mimetype"""
        filetype = mimetypes.guess_type(req.path, strict=True)[0]
        resp.content_type = filetype
        file = read(req.path)

        if file:
            resp.body = file
        else:
            resp.status = falcon.HTTP_404
