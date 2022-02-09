import falcon
import jinja2
from .base import BaseResource
from .html import read


class LoginResource(BaseResource):
    """Falcon resource for user authentication"""

    auth_required = False

    def __init__(self, *args, **kwargs):
        super(LoginResource, self).__init__(*args, **kwargs)

    def on_get(self, req, resp):
        """Get login page"""
        resp.content_type = "text/html"
        file = read("login.html")
        tpl = jinja2.Template(file).render(
            baseurl=self.config.baseurl,
            apiurl=self.config.apiurl,
            loginurl=self.config.loginurl,
            include_register=self.config.include_register,
            registerurl=self.config.registerurl,
            include_password=self.config.include_password,
        )
        resp.body = tpl

    def on_post(self, req, resp):
        """Log user in using authentication backend"""
        token = self.db.users.login(None, req.params, self.session)
        user = self.db.users.detail(token, req.params, self.session)

        if token and user:
            # setup token and set auth cookie
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
            # rerender login page
            resp.content_type = "text/html"
            file = read("login.html")
            tpl = jinja2.Template(file).render(
                baseurl=self.config.baseurl,
                apiurl=self.config.apiurl,
                loginurl=self.config.loginurl,
                include_register=self.config.include_register,
                registerurl=self.config.registerurl,
                include_password=self.config.include_password,
            )
            resp.body = tpl
