from .common import BaseTask
import json
from paperboy.utils import name_to_class
from luigi.parameter import Parameter, ParameterVisibility


class ReportPostTask(BaseTask):
    report = Parameter(visibility=ParameterVisibility.HIDDEN)
    config = Parameter(visibility=ParameterVisibility.HIDDEN)

    def __init__(self, *args, **kwargs):
        super(ReportPostTask, self).__init__(*args, **kwargs)
        config = json.loads(kwargs.get("config", {}))
        self._config = name_to_class(config.get("config")).from_json(config)
        self._report = json.loads(self.report)
        self._completed = False

    def run(self):
        self.log.critical("report-post")

        fp = self.input().open("r")
        output_nb = fp.read()
        fp.close()

        self.log.critical(output_nb)

        outputter = self._config.clazz(self._config)
        outputter.write(self._report, output_nb, task_id=self.task_id)
        self._completed = True
