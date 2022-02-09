import os
import os.path
from datetime import datetime
from .base import BaseOutput


class LocalOutput(BaseOutput):
    """Output to local filesystem"""

    def __init__(self, config, *args, **kwargs):
        self.config = config

    def write(self, report, output, *args, **kwargs):
        task_id = kwargs.get("task_id", "")
        path = (
            os.path.join(self.config.dir, task_id)
            + "_"
            + datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
        )

        if isinstance(report, dict):
            if report["meta"]["output"] == "notebook":
                path += ".ipynb"
            elif report["meta"]["output"] == "script":
                path += ".py"
            elif report["meta"]["output"] == "email":
                path += ".eml"
            elif report["meta"]["output"] in ("pdf", "html"):
                path += ".{}".format(report["meta"]["output"])
        else:
            if report.meta.output == "notebook":
                path += ".ipynb"
            elif report.meta.output == "script":
                path += ".py"
            elif report.meta.output == "email":
                path += ".eml"
            elif report.meta.output in ("pdf", "html"):
                path += ".{}".format(report.meta.output)

        if isinstance(output, bytes):
            output = output.decode("utf8")

        with open(path, "w") as fp:
            fp.write(output)
