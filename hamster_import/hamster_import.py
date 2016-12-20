from .hamster_models import Facts
from project.models import Activity, Customer, Project
try:
    from urllib.request import urlopen
except ImportError:
    from urllib import urlopen
from django.conf import settings
from logging import getLogger

HAMSTER_LOGGER = getLogger('hamster_logger')


def download_hamster_db(url, filename=settings.DATABASES['hamster']['NAME']):
    with urlopen(url) as db_link:
        db_data = db_link.read()
        HAMSTER_LOGGER.info("Successfully downloaded db.")
    with open(filename, 'wb') as db_file:
        db_file.write(db_data)


def import_db_entries():
    customer_names = [c.name.lower() for c in Customer.objects.all()]
    project_names = [p.name.lower() for p in Project.objects.all()]
    for fact in Facts.objects.all():
        if fact.activity.name.lower() not in customer_names:
            continue
        tag = fact.tags[0]
        if tag.name.lower() in project_names:
            description = ''
            if fact.description:
                description = fact.description
            _, created = Activity.objects.get_or_create(
                hamster_id=fact.id,
                start_time=fact.start_time,
                end_time=fact.end_time,
                project=Project.objects.get(name__iexact=tag.name),
                remarks=description)
            if created:
                HAMSTER_LOGGER.info('Created Activitiy with hamster_id {0}'
                                    .format(fact.id))
            else:
                HAMSTER_LOGGER.info('Updated Activitiy with hamster_id {0}'
                                    .format(fact.id))
