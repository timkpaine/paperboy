import logging
import math
from sqlalchemy import or_
from paperboy.config import ListResult


class BaseSQLStorageMixin(object):
    """Base class to share common SQL operations between User/Notebook/Job/Report backends"""

    def _form(self, ConfigCls):
        """Generate form from configuration type.

        Args:
            ConfigCls (paperboy.config.base.Base): UserConfig/NotebookConfig/JobConfig/ReportConfig
        Returns:
            paperboy.config.forms.Response
        """
        return ConfigCls(self.config).form()

    def _search(self, SqlCls, ClsName, user, params, session, *args, **kwargs):
        """Search for a given name in instances of ClsName stored in SQL as type SqlCls

        Args:
            SqlCls (BaseSQLStorageMixin + BaseStorage): Class implementing the BaseStorage interface
            ClsName (string): Notebook/Job/Report
            user (paperboy.storage.base.UserStorage): the user access this data
            params (dict): query parameters
            session (sqlalchemy session): the active sqlalchemy session
        Returns:
            list: results with name/id
        """
        name = params.get("name", "")
        count = int(params.get("count", 10))
        if name is None or name == "":
            return []
        nbs = (
            session.query(SqlCls)
            .filter(SqlCls.name.like(lookfor(name)))
            .filter(
                SqlCls.userId == int(user.id)
                or (hasattr(SqlCls, "privacy") and SqlCls.privacy == "public")
            )
            .limit(count)
        )

        return [{"id": ClsName + "-" + str(nb.id), "name": nb.name} for nb in nbs]

    def _list(self, SqlCls, setter, user, params, session, *args, **kwargs):
        """List all instances of a give storage class

        Args:
            SqlCls (BaseSQLStorageMixin + BaseStorage): Class implementing the BaseStorage interface
            setter (string): unused
            user (paperboy.storage.base.UserStorage): the user access this data
            params (dict): query parameters
            session (sqlalchemy session): the active sqlalchemy session
        Returns:
            list of paperboy.config.base.Base: result notebooks/jobs/reports as json
        """
        base = session.query(SqlCls).filter(
            or_(
                SqlCls.userId.like((user.id)),
                (hasattr(SqlCls, "privacy") and SqlCls.privacy == "public"),
            )
        )
        page = int(params.get("page", 1))
        nbs = base[25 * (page - 1) : 25 * page]

        result = ListResult()
        result.total = base.count()
        result.count = len(nbs)
        result.page = page
        result.pages = math.ceil(result.total / 25) if result.count > 0 else 1

        logging.critical(
            "list : {}, result : {} - {}".format(SqlCls, result.total, len(nbs))
        )

        result.results = [x.to_config(self.config) for x in nbs]
        return result.to_json()

    def _detail(self, SqlCls, user, params, session, *args, **kwargs):
        """Get detailed view of instance

        Args:
            SqlCls (BaseSQLStorageMixin + BaseStorage): Class implementing the BaseStorage interface
            user (paperboy.storage.base.UserStorage): the user access this data
            params (dict): query parameters
            session (sqlalchemy session): the active sqlalchemy session
        Returns:
            edit of paperboy.config.base.Base: notebook/job/report config edit
        """
        id = justid(params.get("id") or -1)
        try:
            id = int(id)
        except ValueError:
            return {}

        if id < 0:
            return {}

        nb_sql = session.query(SqlCls).get(id)  # FIXME permission?

        logging.critical("detail : {}, result : {}".format(id, nb_sql))

        if nb_sql:
            return nb_sql.to_config(self.config).edit()
        return {}


def lookfor(s):
    """Helpful matcher for sqlalchemy query"""
    if "*" in s or "_" in s:
        return s.replace("_", "__").replace("*", "%").replace("?", "_")
    return "%{0}%".format(s)


def justid(id):
    """Helper method to turn name-id string into just id"""
    if isinstance(id, int):
        return id
    if "-" in id:
        return id.split("-", 1)[-1]
    return id
