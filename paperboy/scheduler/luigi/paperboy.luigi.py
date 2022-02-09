# This is the jinja2 templatized set of tasks that
# generates the job. It has the following form as an
# example:
#
#    Job -> Report -> Papermill -> NBConvert ->      ReportPost -\
#      \--> Report -> Papermill -> Voila -> Dokku -> ReportPost --\
#       \-> Report -> Papermill -> NBConvert ->      ReportPost ----> Job Cleanup
#

import luigi
import os
import os.path
import json
from base64 import b64decode

# Base Job Tasks
from paperboy.scheduler.luigi.luigi_tasks import JobTask, JobCleanupTask

# Base Report Tasks
from paperboy.scheduler.luigi.luigi_tasks import ReportTask, ReportPostTask

# Convert Tasks
from paperboy.scheduler.luigi.luigi_tasks import PapermillTask, NBConvertTask

# Publish operators
from paperboy.scheduler.luigi.luigi_tasks import VoilaTask, DokkuTask

from datetime import datetime

###################################
# Inline job and reports as b64 json  #
###################################
job_string = b64decode({{job_json}})
job_json = json.loads(job_string)
reports_string = b64decode({{report_json}})
reports_json = json.loads(reports_string)

interval = "{{interval}}"
start_date = datetime.strptime("{{start_date}}", "%m/%d/%Y %H:%M:%S")
owner = "{{owner}}"
email = "{{email}}"


###################################
# Create dag from job and reports #
###################################
def build():
    # The Job task, used for bundling groups of reports,
    # setting up env/image
    job = JobTask(job=job_string, task_id="Job-{}".format(job_json["id"]))

    cleanup_requires = []

    for rep in reports_json:
        # copy over notebook text (only store 1 copy in the job json)
        rep["meta"]["notebook_text"] = job_json["meta"]["notebook_text"]

        # type is "convert" for nbconversion jobs and "publish" for publish jobs
        type = rep["meta"]["type"]

        # Report task, performs the required
        # steps prior to running the report
        r = ReportTask(report=json.dumps(rep), task_id="Report-{}".format(rep["id"]))
        r._reqs = job

        # Papermill task, performs the report creation
        # using papermill and the report's individual
        # parameters and configuration
        pp = PapermillTask(
            report=json.dumps(rep), task_id="ReportPapermill-{}".format(rep["id"])
        )
        pp._reqs = r

        if type == "convert":
            # NBConvert task, performs the NBConversion if
            # required
            nb = NBConvertTask(
                report=json.dumps(rep), task_id="ReportNBConvert-{}".format(rep["id"])
            )
            nb._reqs = pp

        elif type == "publish":
            # Dokku deployment task, performs the
            # deploy to the dokku repo
            d = DokkuTask(
                report=json.dumps(rep), task_id="ReportDokku-{}".format(rep["id"])
            )
            d._reqs = pp

            # Assemble a Voila Job from papermilled notebook
            nb = VoilaTask(
                report=json.dumps(rep), task_id="ReportVoila-{}".format(rep["id"])
            )
            nb._reqs = d

        else:
            raise NotImplementedError()

        # The post-report task, used for post-report
        # tasks such as sending the report in an email
        # or pushing the deploy to dokku

        # FIXME
        rp = ReportPostTask(
            report=json.dumps(rep),
            config='{"type": "local", "dir": "'
            + os.path.expanduser("~/Downloads")
            + '", "clazz": "paperboy.output.local.LocalOutput", "config": "paperboy.config.output.LocalOutputConfig"}',
            task_id="ReportPost-{}".format(rep["id"]),
        )
        rp._reqs = nb
        cleanup_requires.append(rp)

    # The cleanup task, run after all reports are finished
    cleanup = JobCleanupTask(
        job=job_string,
        task_id="JobCleanup-{}".format(job_json["id"]),
        owner=owner,
        start_date=start_date,
        interval=interval,
        email=email,
    )
    cleanup._reqs = cleanup_requires
    cleanup.time = datetime.now()
    return cleanup


if __name__ == "__main__":
    luigi.build([build()])
