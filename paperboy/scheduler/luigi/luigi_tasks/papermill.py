from .common import BaseTask
import json
import luigi
from luigi.parameter import Parameter, ParameterVisibility


class PapermillTask(BaseTask):
    report = Parameter(visibility=ParameterVisibility.HIDDEN)

    def __init__(self, *args, **kwargs):
        super(PapermillTask, self).__init__(*args, **kwargs)
        self._report = json.loads(self.report)

    def run(self):
        self.log.critical("papermill")

        from paperboy.worker import run_papermill

        ret = run_papermill(
            self._report["meta"]["notebook"],
            self._report["meta"]["notebook_text"],
            self._report["meta"]["parameters"],
            self._report["meta"]["strip_code"],
        )

        fp = self.output().open("w")
        fp.write(ret)
        fp.close()
        self._completed = True

    def output(self):
        return luigi.LocalTarget(self._report["name"])
