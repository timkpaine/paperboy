import os
import getpass


def schedule_cron(command, interval, crontab=None):
    from crontab import CronTab, CronItem

    if not os.path.exists(crontab):
        with open(crontab, "w"):
            pass

    if crontab:
        c = CronTab(tabfile=crontab)
    else:
        c = CronTab(user=getpass.getuser())

    job = CronItem.from_line(interval + " " + command, cron=c)

    c.append(job)
    c.write()
    return c, job


def unschedule_cron(command, crontab=None):
    from crontab import CronTab

    if crontab:
        c = CronTab(tabfile=crontab)
    else:
        c = CronTab(user=getpass.getuser())

    for line in c.lines:
        if str(line) == command:
            line.delete()
            c.write()
            return True
    return False
