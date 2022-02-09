# This is the jinja2 templatized DAG that generates
# the job operator. It has the following form as an
# example:
#
#    Job -> Report -> Papermill -> NBConvert ->      ReportPost -\
#      \--> Report -> Papermill -> Voila -> Dokku -> ReportPost --\
#       \-> Report -> Papermill -> NBConvert ->      ReportPost ----> Job Cleanup
#

import json
from base64 import b64decode

# Base Job Operators
from paperboy.scheduler.airflow_operators import JobOperator, JobCleanupOperator

# Base Report Operators
from paperboy.scheduler.airflow_operators import ReportOperator, ReportPostOperator

# Convert Operators
from paperboy.scheduler.airflow_operators import PapermillOperator, NBConvertOperator

# Publish operators
from paperboy.scheduler.airflow_operators import VoilaOperator, DokkuOperator

from airflow import DAG
from datetime import timedelta, datetime


###################################
# Default arguments for operators #
###################################

# DAG args: https://airflow.incubator.apache.org/code.html?highlight=dag#airflow.models.DAG
dag_args = {
    "description": "",
    "schedule_interval": "{{interval}}",
    "start_date": datetime.strptime("{{start_date}}", "%m/%d/%Y %H:%M:%S"),
    "end_date": None,
    "full_filepath": None,
    "template_searchpath": None,
    "user_defined_macros": None,
    "user_defined_filters": None,
    "concurrency": 16,
    "max_active_runs": 16,
    "dagrun_timeout": None,
    "sla_miss_callback": None,
    "default_view": "graph",
    "orientation": "LR",
    "catchup": False,
    "on_success_callback": None,
    "on_failure_callback": None,
    # 'params': None,
}

# Operator args: https://airflow.incubator.apache.org/code.html#baseoperator
default_operator_args = {
    "owner": "{{owner}}",
    "email": ["{{email}}"],
    "email_on_retry": False,
    "email_on_failure": True,
    "retries": 0,
    "retry_delay": timedelta(minutes=1),
    "retry_exponential_backoff": False,
    "max_retry_delay": None,
    "start_date": None,
    "end_date": None,
    "schedule_interval": None,
    "depends_on_past": False,
    "wait_for_downstream": False,
    # 'params': None,
    "default_args": None,
    "adhoc": False,
    "priority_weight": 1,
    "weight_rule": "downstream",
    "queue": "default",
    "pool": None,
    "sla": None,
    "execution_timeout": None,
    "on_failure_callback": None,
    "on_success_callback": None,
    "on_retry_callback": None,
    "trigger_rule": "all_success",
    "resources": None,
    "run_as_user": None,
    "task_concurrency": None,
    "executor_config": None,
    "inlets": None,
    "outlets": None,
}

###################################
# Inline job and reports as b64 json  #
###################################
job_json = json.loads(b64decode({{job_json}}))
reports_json = json.loads(b64decode({{report_json}}))

###################################
# Create dag from job and reports #
###################################

# The top level dag, representing a Job run on a Notebook
dag = DAG("DAG-" + str(job_json["id"]), default_args=default_operator_args, **dag_args)

# The Job operator, used for bundling groups of reports,
# setting up env/image
job = JobOperator(job=job_json, task_id="Job-{}".format(job_json["id"]), dag=dag)

# The cleanup operator, run after all reports are finished
cleanup = JobCleanupOperator(
    job=job_json, task_id="JobCleanup-{}".format(job_json["id"]), dag=dag
)

for rep in reports_json:
    # copy over notebook text (only store 1 copy in the job json)
    rep["meta"]["notebook_text"] = job_json["meta"]["notebook_text"]

    # type is "convert" for nbconversion jobs and "publish" for publish jobs
    type = rep["meta"]["type"]

    # Report operator, performs the required
    # steps prior to running the report
    r = ReportOperator(report=rep, task_id="Report-{}".format(rep["id"]), dag=dag)
    job.set_downstream(r)

    # Papermill operator, performs the report creation
    # using papermill and the report's individual
    # parameters and configuration
    pp = PapermillOperator(
        report=rep, task_id="ReportPapermill-{}".format(rep["id"]), dag=dag
    )
    r.set_downstream(pp)

    # The post-report operator, used for post-report
    # tasks such as sending the report in an email
    # or pushing the deploy to dokku
    rp = ReportPostOperator(
        report=rep,
        config=json.loads("{{output_config}}"),
        task_id="ReportPost-{}".format(rep["id"]),
        dag=dag,
    )
    rp.set_downstream(cleanup)

    if type == "convert":
        # NBConvert operator, performs the NBConversion if
        # required
        nb = NBConvertOperator(
            report=rep, task_id="ReportNBConvert-{}".format(rep["id"]), dag=dag
        )
        pp.set_downstream(nb)
        nb.set_downstream(rp)

    elif type == "publish":
        # Assemble a Voila Job from papermilled notebook
        v = VoilaOperator(
            report=rep, task_id="ReportVoila-{}".format(rep["id"]), dag=dag
        )
        pp.set_downstream(v)

        # Dokku deployment operator, performs the
        # deploy to the dokku repo
        d = DokkuOperator(
            report=rep, task_id="ReportDokku-{}".format(rep["id"]), dag=dag
        )
        v.set_downstream(d)
        d.set_downstream(rp)

    else:
        raise NotImplementedError()
