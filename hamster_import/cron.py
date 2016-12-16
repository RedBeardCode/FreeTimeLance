import os

from django.conf import settings
from django_cron import CronJobBase, Schedule

from hamster_import.hamster_import import HAMSTER_LOGGER
from hamster_import.hamster_import import download_hamster_db
from hamster_import.hamster_import import import_db_entries


class ImportJob(CronJobBase):
    RUN_EVERY_MINS = 1 if settings.DEBUG else 360
    RETRY_AFTER_FAILURE_MINS = 5
    code = "hamster_import.cron.ImportJob"

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS,
                        retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)

    def do(self):
        HAMSTER_LOGGER.error('Start import job')
        url = os.environ['HAMSTER_URL']
        download_hamster_db(url)
        import_db_entries()
        HAMSTER_LOGGER.info('Stop import job')
