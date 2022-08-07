from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore())
    register_events(scheduler)
    scheduler.start()
