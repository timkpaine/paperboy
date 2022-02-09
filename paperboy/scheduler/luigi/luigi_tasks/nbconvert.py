from .common import BaseTask
import json
import luigi
from luigi.parameter import Parameter, ParameterVisibility


class NBConvertTask(BaseTask):
    report = Parameter(visibility=ParameterVisibility.HIDDEN)

    def __init__(self, *args, **kwargs):
        super(NBConvertTask, self).__init__(*args, **kwargs)
        self._report = json.loads(self.report)

    def run(self):
        self.log.critical("nbconvert")

        fp = self.input().open("r")
        papermilled = fp.read()
        fp.close()

        if self._report["meta"]["output"] != "notebook":
            from paperboy.worker import run_nbconvert

            template = self._report["meta"].get("template", "")

            ret = run_nbconvert(
                self._report["meta"]["notebook"],
                papermilled,
                self._report["meta"]["output"],
                template,
                self._report["meta"]["strip_code"],
            )
        else:
            ret = papermilled

        fp = self.output().open("w")
        fp.write(ret.decode("utf8"))
        fp.close()
        self._completed = True

    def output(self):
        return luigi.LocalTarget(self._report["name"])
