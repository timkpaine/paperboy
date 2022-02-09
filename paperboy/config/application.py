import falcon
import logging
import os
from six.moves.urllib_parse import urljoin
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from traitlets.config.application import Application
from traitlets import Int, Instance, List, Tuple, Unicode, Bool, validate, TraitError
from uuid import uuid4

# falcon api
from ..server.api import FalconAPI

# deployer
from ..server.deploy import FalconDeploy

# base configs
from .user import UserConfig
from .notebook import NotebookConfig
from .job import JobConfig
from .report import ReportConfig
from .scheduler import (
    SchedulerConfig,
    DummySchedulerConfig,
    AirflowSchedulerConfig,
    LuigiSchedulerConfig,
    LocalSchedulerConfig,
)
from .storage import SQLAStorageConfig
from .output import LocalOutputConfig

# no auth
from ..middleware import NoUserMiddleware, NoAuthRequiredMiddleware

# essential middleware
from ..middleware import CORSMiddleware, MultipartMiddleware

# sql
from ..storage.sqla import Base
from ..storage.sqla import (
    UserSQLStorage,
    NotebookSQLStorage,
    JobSQLStorage,
    ReportSQLStorage,
)
from ..middleware import (
    SQLAlchemySessionMiddleware,
    SQLUserMiddleware,
    SQLAuthRequiredMiddleware,
)


class Paperboy(Application):
    """Base class for paperboy applications"""

    name = "paperboy"
    description = "paperboy"

    ############
    # Gunicorn #
    ############
    workers = Int(default_value=1, help="Number of gunicorn workers").tag(config=True)
    port = Unicode(default_value="8080", help="Port to run on").tag(config=True)
    ############

    ##########
    # Falcon #
    ##########
    api = Instance(falcon.API, help="A Falcon API instance").tag(config=True)
    ##########

    ########
    # URLs #
    ########
    baseurl = Unicode(default_value="/", help="Base URL (for reverse proxies)").tag(
        config=True
    )
    apiurl = Unicode(
        default_value="/api/v1/", help="API base URL (for reverse proxies)"
    ).tag(config=True)
    loginurl = Unicode(default_value="login", help="login url").tag(config=True)
    logouturl = Unicode(default_value="logout", help="logout url").tag(config=True)
    registerurl = Unicode(default_value="register", help="register url").tag(
        config=True
    )
    ########

    ########
    # Auth #
    ########
    http = Bool(
        default_value=True,
        help="Running on HTTP (as opposed to https, so token is insecure)",
    ).tag(config=True)
    include_password = Bool(default_value=False).tag(config=True)
    include_register = Bool(default_value=True).tag(config=True)
    token_timeout = Int(default_value=600).tag(config=True)
    #############

    ##########
    # Config #
    ##########
    # FIXME doesnt allow default_value yet
    user_config = UserConfig
    notebook_config = NotebookConfig
    job_config = JobConfig
    report_config = ReportConfig
    ##########

    ##############
    # Middleware #
    ##############
    essential_middleware = [
        CORSMiddleware(allow_all_origins=True).middleware,
        MultipartMiddleware(),
    ]
    extra_middleware = List(default_value=[])  # List of extra middlewares to install
    auth_required_middleware = Instance(object)
    load_user_middleware = Instance(object)
    ##############

    ##################
    # Custom handler #
    ##################
    extra_handlers = List(
        trait=Tuple(), default_value=[]
    )  # List of tuples (route, handler) of handlers to install
    ##################

    ##########################################
    #        Predefined Configurations       #
    #
    ##########################################
    backend = Unicode(
        default_value="dummy", help="Backend set to use, options are {sqla, custom}"
    ).tag(config=True)
    scheduler = Unicode(
        default_value="dummy",
        help="Scheduler type to use, options are {dummy, airflow, luigi}",
    ).tag(config=True)
    auth = Unicode(
        default_value="dummy",
        help="Authentication backend set to use, options are {none, sqla, custom}",
    ).tag(config=True)
    secret = Unicode()

    @validate("backend")
    def _validate_backend(self, proposed):
        if proposed["value"] not in (
            "custom",
            "dummy",
            "git",
            "sqla",
        ):
            raise TraitError("backend not recognized: {}".format(proposed["value"]))
        return proposed["value"]

    @validate("auth")
    def _validate_auth(self, proposed):
        if proposed["value"] not in (
            "custom",
            "none",
            "sqla",
        ):
            raise TraitError("backend not recognized: {}".format(proposed["value"]))
        return proposed["value"]

    ##########################################

    ###########
    # Storage #
    ###########
    # FIXME doesnt allow default_value yet
    storage = SQLAStorageConfig()
    dev = Bool(default_value=False)
    ###########

    #############
    # Scheduler #
    #############
    # FIXME doesnt allow default_value yet
    scheduler_config = Instance(klass=SchedulerConfig, args=(), kwargs={})
    #############

    ##################
    # Output         #
    ##################
    output = Instance(klass=LocalOutputConfig, args=(), kwargs={})
    ##################

    def start(self):
        """Start the whole thing"""
        self.port = os.environ.get("PORT", self.port)

        options = {"bind": "0.0.0.0:{}".format(self.port), "workers": self.workers}
        self.secret = str(uuid4())

        if self.dev:
            self.sql_url = "sqlite:///:memory:"
            logging.critical("Using SQL in memory backend")

            self.storage.engine = create_engine(self.storage.sql_url, echo=False)
            Base.metadata.create_all(self.storage.engine)

            self.sessionmaker = sessionmaker(bind=self.storage.engine)
            self.backend = "sqla"
            self.auth = "sqla"
            self.extra_middleware = self.extra_middleware + [
                SQLAlchemySessionMiddleware(self.storage.sessionmaker)
            ]
            self.storage.notebook_storage = NotebookSQLStorage
            self.storage.job_storage = JobSQLStorage
            self.storage.report_storage = ReportSQLStorage
            self.storage.user_storage = UserSQLStorage
            self.storage.sql_user = True

            logging.critical("Using SQL auth")
            self.auth_required_middleware = SQLAuthRequiredMiddleware
            self.load_user_middleware = SQLUserMiddleware

            logging.critical("Using Dummy scheduler")
            self.scheduler = "dummy"
            self.scheduler_config = DummySchedulerConfig()

        else:

            # Preconfigured storage backends
            if self.backend == "git":
                logging.critical("Using Git backend")
                raise NotImplementedError()

            # default to sqla
            # elif self.backend == 'sqla':
            else:
                logging.critical("Using SQL backend")

                self.storage.engine = create_engine(
                    os.environ.get("PAPERBOY_SQL_URL") or self.storage.sql_url,
                    echo=False,
                )
                Base.metadata.create_all(self.storage.engine)

                self.storage.sessionmaker = sessionmaker(bind=self.storage.engine)
                self.extra_middleware = self.extra_middleware + [
                    SQLAlchemySessionMiddleware(self.storage.sessionmaker)
                ]
                self.storage.notebook_storage = NotebookSQLStorage
                self.storage.job_storage = JobSQLStorage
                self.storage.report_storage = ReportSQLStorage
                self.storage.user_storage = UserSQLStorage
                self.storage.sql_user = True
                self.auth = "sqla"

            # Preconfigured auth backends
            if self.auth == "none":
                logging.critical("Using No auth")
                self.auth_required_middleware = NoAuthRequiredMiddleware
                self.load_user_middleware = NoUserMiddleware

            elif self.auth == "sqla":
                logging.critical("Using SQL auth")
                self.auth_required_middleware = SQLAuthRequiredMiddleware
                self.load_user_middleware = SQLUserMiddleware

            if self.scheduler == "dummy":
                logging.critical("Using dummy scheduler")
                self.scheduler_config = DummySchedulerConfig()

            elif self.scheduler == "airflow":
                logging.critical("Using Airflow scheduler")
                self.scheduler_config = AirflowSchedulerConfig()

            elif self.scheduler == "luigi":
                logging.critical("Using Luigi scheduler")
                self.scheduler_config = LuigiSchedulerConfig()

            elif self.scheduler == "local":
                logging.critical("Using Local scheduler")
                self.scheduler_config = LocalSchedulerConfig()

            else:
                raise Exception("Must specify a valid scheduler!")

        FalconDeploy(FalconAPI(self), options).run()

    @classmethod
    def launch_instance(cls, argv=None, **kwargs):
        """Launch an instance of a Paperboy Application"""
        return super(Paperboy, cls).launch_instance(argv=argv, **kwargs)

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "workers": self.workers,
            "port": self.port,
        }

    aliases = {
        "workers": "Paperboy.workers",
        "port": "Paperboy.port",
        "baseurl": "Paperboy.baseurl",
        "backend": "Paperboy.backend",
        "scheduler": "Paperboy.scheduler",
        "auth": "Paperboy.auth",
        "sql_url": "Paperboy.storage.sql_url",
    }

    def _login_redirect(config, *args, **kwargs):
        raise falcon.HTTPFound(urljoin(config.baseurl, config.loginurl))
