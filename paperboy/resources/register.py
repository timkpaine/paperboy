import falcon
import jinja2
from .base import BaseResource
from .html import read


class RegisterResource(BaseResource):
    auth_required = False

    def __init__(self, *args, **kwargs):
        super(RegisterResource, self).__init__(*args, **kwargs)

    def on_get(self, req, resp):
        """get registration page"""
        resp.content_type = "text/html"
        file = read("register.html")
        tpl = jinja2.Template(file).render(
            baseurl=self.config.baseurl,
            apiurl=self.config.apiurl,
            registerurl=self.config.registerurl,
            include_password=self.config.include_password,
        )
        resp.body = tpl

    def on_post(self, req, resp):
        """register a new user with storage backend"""
        token = self.db.users.store(None, req.params, self.session)
        user = self.db.users.detail(token, req.params, self.session)

        if token and user:
            # create user, login, and set auth token
            req.context["auth_token"] = token
            req.context["user"] = user
            resp.set_cookie(
                "auth_token",
                token,
                max_age=self.config.token_timeout,
                path="/",
                secure=not self.config.http,
            )
            resp.status = falcon.HTTP_302
            resp.set_header("Location", self.config.baseurl)
        else:
            # rerender registration page
            resp.content_type = "text/html"
            file = read("register.html")
            tpl = jinja2.Template(file).render(
                baseurl=self.config.baseurl,
                apiurl=self.config.apiurl,
                registerurl=self.config.registerurl,
                include_password=self.config.include_password,
            )
            resp.body = tpl
