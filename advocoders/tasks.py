from celery.task.schedules import crontab
from celery.decorators import periodic_task
from advocoders import utils


@periodic_task(run_every=crontab(hour='*/4', minute='0', day_of_week='*'))
def update_feeds():
    utils.update_feeds()
