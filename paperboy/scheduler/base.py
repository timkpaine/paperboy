from abc import abstractmethod, ABCMeta
from random import choice
from six import with_metaclass
from ..config.base import Interval


def interval_to_cron(interval, start_time):
    if isinstance(interval, str):
        interval = Interval(interval)
    if interval == Interval.MINUTELY:
        # simple
        return "*/1 * * * *"
    elif interval == Interval.FIVE_MINUTES:
        return "{start_minute_mod_five}-59/5 * * * *".format(
            start_minute_mod_five=start_time.minute % 5
        )
    elif interval == Interval.TEN_MINUTES:
        return "{start_minute_mod_ten}-59/10 * * * *".format(
            start_minute_mod_ten=start_time.minute % 10
        )
    elif interval == Interval.THIRTY_MINUTES:
        return "{start_minute_mod_thirty}-59/30 * * * *".format(
            start_minute_mod_thirty=start_time.minute % 30
        )
    elif interval == Interval.HOURLY:
        return "{start_minute} */1 * * *".format(start_minute=start_time.minute)
    elif interval == Interval.TWO_HOURS:
        return "{start_minute} {start_hour_mod_two}-23/2 * * *".format(
            start_minute=start_time.minute, start_hour_mod_two=start_time.hour % 2
        )
    elif interval == Interval.THREE_HOURS:
        return "{start_minute} {start_hour_mod_three}-23/3 * * *".format(
            start_minute=start_time.minute, start_hour_mod_three=start_time.hour % 3
        )
    elif interval == Interval.SIX_HOURS:
        return "{start_minute} {start_hour_mod_six}-23/6 * * *".format(
            start_minute=start_time.minute, start_hour_mod_six=start_time.hour % 6
        )
    elif interval == Interval.TWELVE_HOURS:
        return "{start_minute} {start_hour_mod_twelve}-23/12 * * *".format(
            start_minute=start_time.minute, start_hour_mod_twelve=start_time.hour % 12
        )
    elif interval == Interval.DAILY:
        return "{start_minute} {start_hour} * * *".format(
            start_minute=start_time.minute, start_hour=start_time.hour
        )
    elif interval == Interval.WEEKLY:
        return "{start_minute} {start_hour} * * {day_of_week}".format(
            start_minute=start_time.minute,
            start_hour=start_time.hour,
            day_of_week=start_time.strftime("%a"),
        )
    elif interval == Interval.MONTHLY:
        return "{start_minute} {start_hour} {start_day} * *".format(
            start_minute=start_time.minute,
            start_hour=start_time.hour,
            start_day=start_time.day,
        )
    else:
        raise Exception("Unknown interval: %s" % interval)


class BaseScheduler(with_metaclass(ABCMeta)):
    """Scheduler abstract base class"""

    def __init__(self, config, db, *args, **kwargs):
        self.config = config
        self.db = db

    @abstractmethod
    def status(self, req, resp, *args, **kwargs):
        """Get status for a given request
        Args:
            req (falcon Request)
            resp (falcon response)
        """
        pass

    @abstractmethod
    def schedule(self, user, notebook, job, reports, *args, **kwargs):
        """Schedule a job to generate reports for notebook and user
        Args:
            user (paperboy.config.User): user requesting the scheduling
            notebook (paperboy.config.Notebook): Notebook for the job
            job (paperboy.config.Job): Job parameters
            reports ([paperboy.config.Report]): Report configurations with parameters
        """
        pass

    @abstractmethod
    def unschedule(self, user, notebook, job, reports, *args, **kwargs):
        """Unschedule a job to generate reports for notebook and user
        Args:
            user (paperboy.config.User): user requesting the scheduling
            notebook (paperboy.config.Notebook): Notebook for the job
            job (paperboy.config.Job): Job parameters
            reports ([paperboy.config.Report]): Report configurations with parameters
        """
        pass


class DummyScheduler(BaseScheduler):
    """Dummy Scheduler class"""

    def __init__(self, config, db, *args, **kwargs):
        self.config = config
        self.db = db

    def status(self, user, params, session, *args, **kwargs):
        """Get status for a given request
        Args:
            req (falcon Request)
            resp (falcon response)
        """
        type = params.get("type", "")
        gen = DummyScheduler.fakequery()
        if type == "jobs":
            return gen["jobs"]
        elif type == "reports":
            return gen["reports"]
        else:
            return gen

    @staticmethod
    def fakequery():
        """If airflow not present, fake the results for now so the UI looks ok"""
        ret = {"jobs": [], "reports": []}
        for i in range(10):
            ret["jobs"].append(
                {
                    "name": "DAG-Job-{}".format(i),
                    "id": "Job-{}".format(i),
                    "meta": {
                        "id": "Job-{}".format(i),
                        "execution": "01/02/2018 12:25:31",
                        "status": choice(["✔", "✘"]),
                    },
                }
            )
            ret["reports"].append(
                {
                    "name": "Report-{}".format(i),
                    "id": "Report-{}".format(i),
                    "meta": {
                        "run": "01/02/2018 12:25:31",
                        "status": choice(["✔", "✘"]),
                        "type": choice(["Post", "Papermill", "NBConvert", "Setup"]),
                    },
                }
            )
        return ret

    def schedule(self, user, notebook, job, reports, *args, **kwargs):
        """Schedule a job to generate reports for notebook and user
        Args:
            user (paperboy.config.User): user requesting the scheduling
            notebook (paperboy.config.Notebook): Notebook for the job
            job (paperboy.config.Job): Job parameters
            reports ([paperboy.config.Report]): Report configurations with parameters
        """
        pass

    def unschedule(self, user, notebook, job, reports, *args, **kwargs):
        """Unschedule a job to generate reports for notebook and user
        Args:
            user (paperboy.config.User): user requesting the scheduling
            notebook (paperboy.config.Notebook): Notebook for the job
            job (paperboy.config.Job): Job parameters
            reports ([paperboy.config.Report]): Report configurations with parameters
        """
        pass
