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
from sqlalchemy.orm import sessionmaker, scoped_session

_session_maker = sessionmaker()
_session = scoped_session(_session_maker)


class LoadUserMiddleware:
    """Load a user from the database during the request cycle using sqlalchemy

    By default this will grab the id data from the auth token on the request
    context assuming you are using `.middleware.auth_required`. To change that
    pass a function which takes the request and returns the user id to `get_id`.

    :param session: a sqlalchemy session
    :param user_cls: a class which will return the user object. This object must
        have a `get_by_id` which will return a SQLAlchemy Query.
    :param get_id: a function which will get the user identifier off of the
        request.

    """

    def __init__(self, user_cls, get_id=None, session=None):
        self.user_cls = user_cls
        self.get_id = get_id or self._get_id
        self.session = session or _session

    @staticmethod
    def _get_id(req):
        try:
            return req.context.get("auth_token_contents").get("sub")
        except AttributeError:
            return None

    def fetch_user(self, user_id):
        return (
            self.user_cls.get_by_id(user_id).with_session(self.session()).one_or_none()
        )

    def process_request(self, req, resp):
        user_id = self.get_id(req)
        req.context["user"] = self.fetch_user(user_id)
