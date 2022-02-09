from enum import Enum
from functools import lru_cache
from traitlets import HasTraits


class BaseEnum(Enum):
    @classmethod
    @lru_cache(None)
    def members(cls):
        return cls.__members__.keys()

    @classmethod
    @lru_cache(None)
    def values(cls):
        return tuple(x.value for x in cls.__members__.values())


class Interval(BaseEnum):
    MINUTELY = "minutely"
    FIVE_MINUTES = "5 minutes"
    TEN_MINUTES = "10 minutes"
    THIRTY_MINUTES = "30 minutes"
    HOURLY = "hourly"
    TWO_HOURS = "2 hours"
    THREE_HOURS = "3 hours"
    SIX_HOURS = "6 hours"
    TWELVE_HOURS = "12 hours"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class ReportType(BaseEnum):
    CONVERT = "convert"
    # PUBLISH = 'publish'


class OutputType(BaseEnum):
    NOTEBOOK = "notebook"
    PDF = "pdf"
    HTML = "html"
    EMAIL = "email"
    SCRIPT = "script"
    # POWERPOINT = 'powerpoint'


class PrivacyLevel(BaseEnum):
    PUBLIC = "public"
    PRIVATE = "private"


class ServiceLevel(BaseEnum):
    PRODUCTION = "production"
    RESEARCH = "research"
    DEVELOPMENT = "development"
    PERSONAL = "personal"


_INTERVAL_TYPES = Interval.values()
_REPORT_TYPES = ReportType.values()
_OUTPUT_TYPES = OutputType.values()
_PRIVACY_LEVELS = PrivacyLevel.values()
_SERVICE_LEVELS = ServiceLevel.values()


class Base(HasTraits):
    """Base HasTraits abstract base class for all paperboy configureables (User, Notebook, Job, and Report)"""

    def __init__(self, config, *args, **kwargs):
        super(Base, self).__init__(*args, **kwargs)
        self.config = config

    @staticmethod
    def from_json(jsn, config):
        """create a paperboy config object from a json

        Args:
            jsn: python dictionary from json representing the configuration object
            config: paperboy configuration to populate from json

        Returns:
            subclass of Base populated from jsn
        """
        raise NotImplementedError()

    def to_json(self, include_notebook=False):
        """convert a paperboy config to a json

        Args:
            self: subclass of Base
            include_notebook: if config would include a notebook (potentially several MB in size), should
                we include it or strip it?

        Returns:
            dict: python dictionary representing the response json
        """
        raise NotImplementedError()

    def form(self):
        """generate a JSON form template for the subclass of Base

        Args:
            self: subclass of Base

        Returns:
            dict: python dictionary representing the form template as a JSON
        """
        raise NotImplementedError()

    def edit(self):
        """generate a JSON edit template for the subclass of Base

        Args:
            self: subclass of Base

        Returns:
            dict: python dictionary representing the edit template as a JSON
        """
        raise NotImplementedError()

    def entry(self):
        raise NotImplementedError()

    def store(self):
        raise NotImplementedError()
