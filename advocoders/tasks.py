from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.decorators import task
from advocoders import utils
from advocoders.models import Profile


@periodic_task(run_every=crontab(hour='*/4', minute='0', day_of_week='*'))
def update_feeds():
    utils.update_feeds()


@task
def update_feed(profile_id, provider):
    profile = Profile.objects.get(pk=profile_id)
    if provider == 'blog':
        utils.update_feed(profile, 'blog', profile.blog)
        return
    for social_auth in profile.user.social_auth.all():
        if social_auth.provider == provider:
            utils.update_feed(profile, provider,
                social_auth.extra_data.get('rss_url'))
