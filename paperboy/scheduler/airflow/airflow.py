# -*- coding: utf-8 -*-
import configparser
import json
import os
import os.path
import jinja2
import subprocess
from base64 import b64encode
from sqlalchemy import create_engine
from ..base import BaseScheduler, interval_to_cron

with open(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "paperboy.airflow.py")), "r"
) as fp:
    TEMPLATE = fp.read()

QUERY = """
SELECT task_id, dag_id, execution_date, state, unixname
FROM task_instance
ORDER BY execution_date ASC
LIMIT 20;
"""


class AirflowScheduler(BaseScheduler):
    def __init__(self, *args, **kwargs):
        """Create a new airflow scheduler, connecting to the airflow instances configuration"""
        super(AirflowScheduler, self).__init__(*args, **kwargs)
        cp = configparser.ConfigParser()
        cp.read(self.config.scheduler_config.config)
        try:
            self.sql_conn = cp["core"]["sql_alchemy_conn"]
        except KeyError:
            self.sql_conn = ""

        if self.sql_conn:
            self.engine = create_engine(self.sql_conn)
        else:
            self.engine = None

    def status(self, user, params, session, *args, **kwargs):
        """Get status of job/report DAGs"""
        type = params.get("type", "")
        gen = AirflowScheduler.query(self.engine)
        if type == "jobs":
            return gen["jobs"]
        elif type == "reports":
            return gen["reports"]
        else:
            return gen

    @staticmethod
    def query(engine):
        """Get status of job/report DAGs from airflow\'s database"""
        ret = {"jobs": [], "reports": []}
        with engine.begin() as conn:
            res = conn.execute(QUERY)
            for i, item in enumerate(res):
                ret["jobs"].append(
                    {
                        "name": item[1],
                        "id": item[1][4:],
                        "meta": {
                            "id": item[1][4:],
                            "execution": item[2].strftime("%m/%d/%Y %H:%M:%S"),
                            "status": "✔" if item[3] == "success" else "✘",
                        },
                    }
                )

                report_name = (
                    item[0]
                    .replace("ReportPost-", "")
                    .replace("Report-", "")
                    .replace("ReportNBConvert-", "")
                    .replace("ReportPapermill-", "")
                )

                report_type = (
                    "Post"
                    if "ReportPost" in item[0]
                    else "Papermill"
                    if "Papermill" in item[0]
                    else "NBConvert"
                    if "NBConvert" in item[0]
                    else "Setup"
                )

                ret["reports"].append(
                    {
                        "name": item[0],
                        "id": report_name,
                        "meta": {
                            "run": item[2].strftime("%m/%d/%Y %H:%M:%S"),
                            "status": "✔" if item[3] == "success" else "✘",
                            "type": report_type,
                        },
                    }
                )
            return ret

    @staticmethod
    def template(config, user, notebook, job, reports, *args, **kwargs):
        """jinja templatize airflow DAG for paperboy (paperboy.airflow.py)"""
        owner = user.name
        start_date = job.meta.start_time.strftime("%m/%d/%Y %H:%M:%S")
        email = "test@test.com"
        job_json = b64encode(json.dumps(job.to_json(True)).encode("utf-8"))
        report_json = b64encode(
            json.dumps([r.to_json() for r in reports]).encode("utf-8")
        )
        interval = interval_to_cron(job.meta.interval, job.meta.start_time)

        tpl = jinja2.Template(TEMPLATE).render(
            owner=owner,
            start_date=start_date,
            interval=interval,
            email=email,
            job_json=job_json,
            report_json=report_json,
            output_config=json.dumps(config.output.to_json()),
        )
        return tpl

    def schedule(self, user, notebook, job, reports, *args, **kwargs):
        """Schedule a DAG for `job` composed of `reports` to be run on airflow"""
        template = AirflowScheduler.template(
            self.config, user, notebook, job, reports, *args, **kwargs
        )
        name = job.id + ".py"
        os.makedirs(self.config.scheduler_config.dagbag, exist_ok=True)
        with open(os.path.join(self.config.scheduler_config.dagbag, name), "w") as fp:
            fp.write(template)
        return template

    def unschedule(self, user, notebook, job, reports, *args, **kwargs):
        """Remove the DAG for `user` and `notebook` composed of `job` running `reports` from
        airflow 2 parts, remove the dag from disk and delete the dag from airflow's database using the CLI"""
        if reports:
            # reschedule
            return self.schedule(user, notebook, job, reports, *args, **kwargs)

        else:
            # delete
            name = job.id + ".py"
            file = os.path.join(self.config.scheduler_config.dagbag, name)
            dag = "DAG-" + job.id

            # delete dag file
            os.remove(file)

            # delete dag
            # FIXME
            try:
                cmd = ["airflow", "delete_dag", dag, "-y"]
                subprocess.call(cmd)
            except Exception as e:
                print(e)
