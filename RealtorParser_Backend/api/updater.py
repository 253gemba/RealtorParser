from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import register_events, DjangoJobStore

from .parsers.AvitoParser import AvitoParser
from .parsers.CianParser import CianParser


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), 'djangojobstore')
    register_events(scheduler)

    @scheduler.scheduled_job('interval', minutes=10, name='Avito', next_run_time=datetime.now())
    def parse_avito():
        AvitoParser().run()

    @scheduler.scheduled_job('interval', minutes=10, name='Cian', next_run_time=datetime.now())
    def parse_cian():
        CianParser().run()

    scheduler.start()