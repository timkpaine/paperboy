import jwt
import logging
from paperboy.config import UserConfig
from paperboy.storage import UserStorage
from .base import BaseSQLStorageMixin
from .models.user import UserSQL


class UserSQLStorage(BaseSQLStorageMixin, UserStorage):
    def __init__(self, *args, **kwargs):
        super(UserSQLStorage, self).__init__(*args, **kwargs)

    def status(self, *args, **kwargs):
        """Not used"""
        return {}

    def form(self):
        """Pass through to shared method in BaseSQLStorageMixin"""
        return self._form(UserConfig)

    def search(self, user, params, session, *args, **kwargs):
        """Pass through to shared method in BaseSQLStorageMixin"""
        return self._search(UserSQL, "User", user, params, session, *args, **kwargs)

    def login(self, user, params, session, *args, **kwargs):
        """username/password -> user/token"""
        username = params.get("username")
        password = params.get("password") or ""
        user = (
            session.query(UserSQL).filter_by(name=username, password=password).first()
        )

        if user:
            token = jwt.encode(
                {"id": str(user.id), "name": user.name},
                self.config.secret,
                algorithm="HS256",
            ).decode("ascii")
            return token

    def list(self, user, params, session, *args, **kwargs):
        """Not used"""
        return {}

    def detail(self, user, params, session, *args, **kwargs):
        """token -> user"""
        try:
            user = jwt.decode(user, self.config.secret, algorithms=["HS256"])
        except (jwt.exceptions.InvalidSignatureError, jwt.exceptions.DecodeError):
            return None
        return UserConfig(self.config, name=user["name"], id=user["id"])

    def store(self, user, params, session, *args, **kwargs):
        username = params.get("username")
        password = params.get("password") or ""
        user = UserSQL(name=username, password=password)

        session.add(user)  # may raise exception

        # generate id
        session.flush()
        session.refresh(user)

        token = jwt.encode(
            {"id": str(user.id), "name": user.name},
            self.config.secret,
            algorithm="HS256",
        ).decode("ascii")
        logging.critical("Storing user {} {} {}".format(username, token, user.id))
        return token

    def delete(self, user, params, session, *args, **kwargs):
        user = session.query(UserSQL).filter(UserSQL.id == user.id).first()
        name = user.name
        session.delete(user)
        return [
            {
                "name": "",
                "type": "p",
                "value": "Success!",
                "required": False,
                "readonly": False,
                "hidden": False,
            },
            {
                "name": "",
                "type": "p",
                "value": "Successfully deleted user: " + name,
                "required": False,
                "readonly": False,
                "hidden": False,
            },
        ]
