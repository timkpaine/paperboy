"""Copied from https://gitlab.com/skosh/falcon-helpers due to conda-forge issues
Copyright (c) 2017 by Nicholas Zaccardi

Some rights reserved.

Redistribution and use in source and binary forms of the software as well
as documentation, with or without modification, are permitted provided
that the following conditions are met:

* Redistributions of source code must retain the above copyright
  notice, this list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above
  copyright notice, this list of conditions and the following
  disclaimer in the documentation and/or other materials provided
  with the distribution.

* The names of the contributors may not be used to endorse or
  promote products derived from this software without specific
  prior written permission.

THIS SOFTWARE AND DOCUMENTATION IS PROVIDED BY THE COPYRIGHT HOLDERS AND
CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT
NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER
OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE AND DOCUMENTATION, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
DAMAGE.
"""
import falcon


def _default_failed(req, resp, **kwargs):
    raise falcon.HTTPFound("/auth/login")


class AuthRequiredMiddleware:
    """Requires a cookie be set with a valid JWT or fails

    Example:
        import falcon
        from falcon_helpers.middlewares.auth_required import AuthRequiredMiddleware

        class Resource:
            auth_required = True

            def on_get(self, req, resp):
                # ...

        def when_fails_auth(req, resp, token_value):
            raise TerribleException(token_value)

        api = falcon.API(
            middleware=[
                AuthRequiredMiddleware(when_fails=when_fails_auth)
            ]
        )

        api.add_route('/', Resource())

    Attributes:
        resource_param: The paramater to pull the boolean from

        context_key: the key the token will be found on the request

        when_fails: (function) A function to execute when the authentication
            fails
    """

    def __init__(
        self,
        resource_param="auth_required",
        context_key="auth_token_contents",
        when_fails=_default_failed,
    ):

        self.resource_param = resource_param
        self.context_key = context_key
        self.failed_action = when_fails

    def process_resource(self, req, resp, resource, params):
        required = getattr(resource, self.resource_param, True)
        token_value = req.context.get(self.context_key, None)

        token_value = None if isinstance(token_value, Exception) else token_value

        if required and not token_value:
            return self.failed_action(req=req, resp=resp, token_value=token_value)
