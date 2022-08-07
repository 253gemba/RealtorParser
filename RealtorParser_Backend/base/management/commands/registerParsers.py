from apscheduler.schedulers.background import BackgroundScheduler
from base.parsers.AvitoParser import AvitoParser
from base.parsers.CianParser import CianParser
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore, register_events


class Command(BaseCommand):
    help = 'Register parser jobs'

    def handle(self, *args, **kwargs):
        scheduler = BackgroundScheduler()
        scheduler.add_jobstore(DjangoJobStore())

        scheduler.add_job(AvitoParser().run, 'interval', minutes=5, id='Avito', replace_existing=True, jobstore='default')
        scheduler.add_job(CianParser().run, 'interval', minutes=5, id='Cian', replace_existing=True, jobstore='default')
        register_events(scheduler)
        scheduler.start()
        