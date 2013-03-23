from django.db.models.signals import pre_save
from django.dispatch import receiver
from social_auth.models import UserSocialAuth
from advocoders.models import Profile
from advocoders import tasks


@receiver(pre_save, sender=UserSocialAuth)
def social_auth_extra_values(sender, instance, **kwargs):
    if instance.provider == 'github':
        instance.extra_data['rss_url'] = 'https://github.com/%s.atom' % instance.extra_data.get('login')
    if instance.provider == 'stackoverflow':
        instance.extra_data['rss_url'] = 'http://stackoverflow.com/feeds/user/%s' % instance.uid
    if instance.extra_data.get('rss_url'):
        profile, _ = Profile.objects.get_or_create(user=instance.user)
        tasks.update_feed.delay(profile.id, instance.provider)
    return instance
