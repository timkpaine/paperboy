import logging
from luigi import Task
from luigi.parameter import Parameter, DateParameter, ParameterVisibility


class BaseTask(Task):
    task_id = Parameter()

    def __init__(self, *args, **kwargs):
        super(BaseTask, self).__init__(*args, **kwargs)
        self._reqs = []
        self.log = logging  # FIXME
        self._completed = False

    def requires(self):
        return self._reqs

    def complete(self):
        if self._reqs:
            if isinstance(self._reqs, list):
                return all(r.complete() for r in self._reqs) and self._completed
            return self._reqs.complete() and self._completed
        return self._completed


class JobTask(BaseTask):
    job = Parameter(visibility=ParameterVisibility.HIDDEN)

    def __init__(self, *args, **kwargs):
        super(JobTask, self).__init__(*args, **kwargs)

    def run(self):
        self.log.critical("job")
        self._completed = True


class JobCleanupTask(BaseTask):
    job = Parameter(visibility=ParameterVisibility.HIDDEN)
    interval = Parameter()
    start_date = DateParameter()
    owner = Parameter()
    email = Parameter()
    time = DateParameter()

    def __init__(self, *args, **kwargs):
        super(JobCleanupTask, self).__init__(*args, **kwargs)

    def run(self):
        self.log.critical("job-cleanup")
        self._completed = True


class ReportTask(BaseTask):
    report = Parameter(visibility=ParameterVisibility.HIDDEN)

    def __init__(self, *args, **kwargs):
        super(ReportTask, self).__init__(*args, **kwargs)

    def run(self):
        self.log.critical("report")
        self._completed = True
