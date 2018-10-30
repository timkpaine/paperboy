import json
from base64 import b64decode
from paperboy.scheduler._airflow import JobOperator, JobCleanupOperator, ReportOperator, ReportPostOperator
from airflow import DAG
from datetime import timedelta


###################################
# Default arguments for operators #
###################################
default_args = {
    'owner': '{{owner}}',
    'start_date': '{{start_date}}'.strftime('%m/%d/%Y %H:%M:%S'),
    'email': ['{{email}}'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

###################################
# Inline job and reports as b64 json  #
###################################
job = json.loads(b64decode(b'{{job_json}}'))
reports = json.loads(b64decode(b'{{report_json}}'))


###################################
# Create dag from job and reports #
###################################

# The top level dag, representing a Job run on a Notebook
dag = DAG('DAG_' + str(job['id']), default_args=default_args)

# The Job operator, used for bundling groups of reports,
# setting up env/image
job = JobOperator(task_id=job['id'], dag=dag)

# The cleanup operator, run after all reports are finished
cleanup = JobCleanupOperator(task_id='job_cleanup', dag=dag)

for rep in reports:
    # Report operator, performs the report creation
    # using papermill and the report's individual
    # parameters and configuration
    r = ReportOperator(task_id=rep['id'], dag=dag)

    # The post-report operator, used for post-report
    # tasks such as sending the report in an email,
    # deploying the report to a webserver, etc
    rp = ReportPostOperator(task_id=rep['id'], dag=dag)

    # Job -> Report -> ReportPost -\
    #   \--> Report -> ReportPost --\
    #    \-> Report -> ReportPost ----> Job Cleanup
    job.set_downstream(r)
    r.set_downstream(rp)
    rp.set_downstream(cleanup)