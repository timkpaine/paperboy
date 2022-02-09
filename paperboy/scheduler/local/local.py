# -*- coding: utf-8 -*-
import os
import os.path
from ..base import BaseScheduler, interval_to_cron
from .schedule import LocalProcessScheduler


class LocalScheduler(BaseScheduler):
    def __init__(self, *args, **kwargs):
        """Create a new local scheduler"""
        super(LocalScheduler, self).__init__(*args, **kwargs)
        self.scheduler = LocalProcessScheduler()

    def status(self, user, params, session, *args, **kwargs):
        """Get status of job/report tasks"""
        type = params.get("type", "")

        # TODO
        gen = LocalScheduler.query()
        if type == "jobs":
            return gen.get("jobs", [])
        elif type == "reports":
            return gen.get("reports", [])
        else:
            return gen or {}

    @staticmethod
    def query():
        """Get status of job/reports"""
        return {}

    def schedule(self, user, notebook, job, reports, *args, **kwargs):
        """Schedule a DAG for `job` composed of `reports` to be run locally"""
        # create task
        working_dir = self.config.scheduler_config.working_directory
        job_dir = os.path.join(working_dir, str(job.id))
        os.makedirs(job_dir, exist_ok=True)
        self.scheduler.schedule(
            job,
            reports,
            job_dir,
            interval_to_cron(job.meta.interval, job.meta.start_time),
        )

    def unschedule(self, user, notebook, job, reports, *args, **kwargs):
        """Remove the DAG for `user` and `notebook` composed of `job` running `reports` from
        local"""
        if reports:
            # reschedule
            working_dir = self.config.scheduler_config.working_directory
            job_dir = os.path.join(working_dir, str(job.id))
            os.makedirs(job_dir, exist_ok=True)
            self.scheduler.schedule(
                job,
                reports,
                job_dir,
                interval_to_cron(job.meta.interval, job.meta.start_time),
            )

        else:
            # delete
            self.scheduler.unschedule(job.id)
