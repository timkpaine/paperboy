import os
import os.path
import logging
from paperboy.utils import name_to_class
from ._nbconvert import run as run_nbconvert  # noqa: F401
from ._papermill import run as run_papermill  # noqa: F401


def run(job, reports, working_dir=None):
    logging.critical("Calling run on job - %s" % str(job.id))
    for rep in reports:
        # type is "convert" for nbconversion jobs and "publish" for publish jobs
        type = rep.meta.type

        # Papermill task, performs the report creation
        # using papermill and the report's individual
        # parameters and configuration
        papermilled = run_papermill(
            rep.meta.notebook.name,
            rep.meta.notebook.meta.notebook,
            rep.meta.parameters,
            rep.meta.strip_code,
        )

        if type == "convert":
            # NBConvert task, performs the NBConversion if
            # required
            if rep.meta.output != "notebook":
                template = rep.meta.template

                ret = run_nbconvert(
                    rep.meta.notebook.name,
                    papermilled,
                    rep.meta.output,
                    template,
                    rep.meta.strip_code,
                )
            else:
                ret = papermilled

        elif type == "publish":
            # Dokku deployment task, performs the
            # deploy to the dokku repo
            raise NotImplementedError()

            # Assemble a Voila Job from papermilled notebook
        else:
            raise NotImplementedError()

        # The post-report task, used for post-report
        # tasks such as sending the report in an email
        # or pushing the deploy to dokku

        config = {
            "type": "local",
            "dir": os.path.expanduser("~/Downloads"),
            "clazz": "paperboy.output.local.LocalOutput",
            "config": "paperboy.config.output.LocalOutputConfig",
        }
        config = name_to_class(config["config"]).from_json(config)
        outputter = config.clazz(config)
        outputter.write(rep, ret)
