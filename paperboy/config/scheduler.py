import os
import os.path
import tempfile
from traitlets import HasTraits, Unicode, Bool
from ..scheduler import DummyScheduler, AirflowScheduler, LuigiScheduler, LocalScheduler


class SchedulerConfig(HasTraits):
    """Base config for scheduler"""

    type = Unicode()


class DummySchedulerConfig(SchedulerConfig):
    """Configuration for airflow"""

    type = "dummy"
    clazz = DummyScheduler


class AirflowSchedulerConfig(SchedulerConfig):
    """Configuration for airflow"""

    type = "airflow"
    dagbag = Unicode(default_value=os.path.expanduser("~/airflow/dags"))
    config = Unicode(default_value=os.path.expanduser("~/airflow/airflow.cfg"))
    clazz = AirflowScheduler


class LuigiSchedulerConfig(SchedulerConfig):
    """Configuration for luigi"""

    type = "luigi"
    task_folder = Unicode(default_value=os.path.expanduser("~/luigi/tasks"))
    db_connection = Unicode(
        default_value=os.path.expanduser("sqlite://~/luigi/luigi-task-hist.db")
    )
    state_path = Unicode(default_value=os.path.expanduser("~/luigi/state.pickle"))

    # local or cron for scheduler
    local = Bool(default_value=True)

    crontab = Unicode(default_value=os.path.expanduser("~/luigi/cron.tab"))
    clazz = LuigiScheduler


class LocalSchedulerConfig(SchedulerConfig):
    """Configuration for local scheduler"""

    type = "local"
    working_directory = Unicode(
        default_value=os.path.join(tempfile.gettempdir(), "paperboy")
    )
    clazz = LocalScheduler
