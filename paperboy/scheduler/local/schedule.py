import getpass
import os
import logging
import time
import threading
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue, Empty
from ...worker import run


def interval_to_schedule(cronjob):
    """this function will be called roughly every minute
    and should parse the cronjob's timing to see if the
    job should run in this minute"""
    now = datetime.now()

    # parse minutes first
    minute = str(cronjob.minute)
    hour = str(cronjob.hour)
    day_of_week = str(cronjob.dow)
    day_of_month = str(cronjob.dom)

    ret = (
        _parse(now.minute, minute),
        _parse(now.hour, hour),
        _parse(now.day, day_of_month),
        _parse_dow(now.strftime("%a"), day_of_week),
    )
    if all(ret):
        return True
    return False


def _parse(now, field):
    # run every time?
    if str(field) == "*/1" or str(field) == "*":
        return True

    # else run every interval?
    if "-59" in field:
        splits = field.replace("-59", "").replace("-23", "").split("/")
        base, mod = int(splits[0]), int(splits[1])

        # check if now % mod == base
        if now % mod != base:
            return True
        else:
            return False

    # else run on specific minutes
    field = int(field)
    if field == now:
        return True
    else:
        # not the right minute
        return False


def _parse_dow(now, field):
    # run every time?
    if str(field) == "*" or str(field).upper() == now.upper():
        return True
    return False


def run_tasks(add_queue, delete_queue):
    executor = ThreadPoolExecutor(max_workers=os.cpu_count() - 1)
    tasks = {}
    futures = []
    while True:
        for tid, task in tasks.items():
            job, reports, job_dir, interval, cron = tasks[tid]
            if interval_to_schedule(cron):
                logging.critical("Submitting - %s" % str(job))
                futures.append(executor.submit(run, job, reports, job_dir))

        for future in as_completed(futures):
            logging.critical("Future finished")
            if future.exception():
                raise future.exception()
            else:
                logging.critical(future.result())

        now = datetime.now()
        end = datetime(
            year=now.year,
            month=now.month,
            day=now.day,
            hour=now.hour,
            minute=now.minute,
        ) + timedelta(minutes=1)
        while datetime.now() < end:
            # add to tasks
            while True:
                try:
                    item = add_queue.get_nowait()
                    tasks[item[0].id] = item
                except Empty:
                    break

                # delete tasks
            while True:
                try:
                    item = delete_queue.get_nowait()
                    tasks.pop(item, None)
                except Empty:
                    break
            time.sleep(1)


class LocalProcessScheduler(object):
    def __init__(self):
        self.tasks = {}
        self.add_queue = Queue()
        self.delete_queue = Queue()
        self.runner = None

    def schedule(self, job, reports, job_dir, interval):
        from crontab import CronTab, CronItem

        # must occur in gunicorn process
        if self.runner is None:
            self.runner = threading.Thread(
                target=run_tasks, args=(self.add_queue, self.delete_queue)
            )
            self.runner.daemon = True
            self.runner.start()

        c = CronTab(user=getpass.getuser())
        cjob = CronItem.from_line(interval + " echo test", cron=c)

        self.tasks[job.id] = (job, reports, job_dir, interval, cjob)
        logging.critical("Scheduling job: %s" % str(job.id))
        self.add_queue.put((job, reports, job_dir, interval, cjob))

    def unschedule(self, job_id):
        self.tasks[job_id] = None
        self.delete_queue.put(job_id)
