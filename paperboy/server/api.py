import falcon
from six.moves.urllib_parse import urljoin
from ..resources import (
    StaticResource,
    HTMLResource,
    LoginResource,
    LogoutResource,
    RegisterResource,
)
from ..resources import (
    StatusResource,
    AutocompleteResource,
    ConfigResource,
    SchedulerResource,
)
from ..resources import NotebookResource, JobResource, ReportResource
from ..resources import NotebookDetailResource, JobDetailResource, ReportDetailResource
from ..storage import StorageEngine, StorageError


def FalconAPI(config):
    """Create falcon.API application from Paperboy traitlets application

    Args:
        config (paperboy.config.application.Paperboy): traitlets configuration for application

    Returns:
        falcon.API: the routed falcon api to launch with gunicorn/waitress
    """

    def from_base(url):
        return urljoin(config.baseurl, url)

    def from_api(url):
        return urljoin(config.apiurl, url)

    ###########
    # Storage #
    ###########
    db = StorageEngine(
        config.storage.user_storage(config),
        config.storage.notebook_storage(config),
        config.storage.job_storage(config),
        config.storage.report_storage(config),
    )
    api = falcon.API(
        middleware=[
            config.auth_required_middleware(config, db),
            config.load_user_middleware(config, db),
        ]
        + config.essential_middleware
        + config.extra_middleware
    )
    api.add_error_handler(StorageError, StorageError.handle)

    #############
    # Scheduler #
    #############
    scheduler = config.scheduler_config.clazz(config, db)

    ####################
    # Static resources #
    ####################
    html = HTMLResource(config)
    static = StaticResource(config)
    api.add_route(from_base(""), html)
    api.add_route(from_base("index.html"), html)
    api.add_sink(static.on_get, prefix=from_base("static"))

    ##################
    # Auth Resources #
    ##################
    login = LoginResource(config, db)
    api.add_route(from_base(config.loginurl), login)
    logout = LogoutResource(config, db)
    api.add_route(from_base(config.logouturl), logout)
    register = RegisterResource(config, db)
    api.add_route(from_base(config.registerurl), register)

    ##########
    # Routes #
    ##########
    kwargs = {"config": config, "db": db, "scheduler": scheduler}

    # Status
    status = StatusResource(**kwargs)
    api.add_route(from_api("status"), status)

    # Scheduler
    schedulerresource = SchedulerResource(**kwargs)
    api.add_route(from_api("scheduler"), schedulerresource)

    # Autocomplete
    autocomplete = AutocompleteResource(**kwargs)
    api.add_route(from_api("autocomplete"), autocomplete)

    # Config
    configresource = ConfigResource(**kwargs)
    api.add_route(from_api("config"), configresource)

    # Notebooks
    notebooks = NotebookResource(**kwargs)
    api.add_route(from_api("notebooks"), notebooks)

    notebooksdetail = NotebookDetailResource(**kwargs)
    api.add_route(from_api("notebooks/details"), notebooksdetail)

    # Jobs
    jobs = JobResource(**kwargs)
    api.add_route(from_api("jobs"), jobs)

    jobdetail = JobDetailResource(**kwargs)
    api.add_route(from_api("jobs/details"), jobdetail)

    # Reports
    reports = ReportResource(**kwargs)
    api.add_route(from_api("reports"), reports)

    reportdetail = ReportDetailResource(**kwargs)
    api.add_route(from_api("reports/details"), reportdetail)

    # Extra handlers
    for route, handler in config.extra_handlers:
        api.add_route(route, handler(**kwargs))
    return api
