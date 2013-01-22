from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from social_auth.models import UserSocialAuth


class Company(models.Model):
    domain = models.CharField(max_length=255, unique=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.domain


class Profile(models.Model):
    user = models.OneToOneField(User)
    company = models.ForeignKey(Company, null=True)
    picture = models.ForeignKey(UserSocialAuth, null=True)
    title = models.CharField(max_length=255)
    blog = models.URLField()
    stackoverflow = models.URLField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.user.get_full_name()

    @property
    def company_choices(self):
        return Company.objects.filter(domain__in=self.domains)

    @property
    def domains(self):
        if self.user.email:
            from advocoders import utils
            return [utils.get_domain(self.user.email)]

    @property
    def possible_accounts(self):
        ''' returns a dict of all possible account types and either None
        or this user's account of that type '''
        return dict((provider, self.get_provider_or_none(provider))
            for provider in settings.POSSIBLE_PROVIDERS)

    def get_provider_or_none(self, provider):
        try:
            return self.user.social_auth.get(provider=provider)
        except UserSocialAuth.DoesNotExist:
            return None

    @property
    def rss_urls(self):
        if self.blog:
            yield ('blog', self.blog)
        if self.stackoverflow:
            yield ('stackoverflow', self.stackoverflow)
        for social_auth in self.user.social_auth.all():
            rss_url = social_auth.extra_data.get('rss_url')
            if rss_url:
                yield (social_auth.provider, rss_url)

    @property
    def picture_url(self):
        return self.picture.extra_data.get('picture')


class Content(models.Model):
    user = models.ForeignKey(User)
    provider = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    link = models.URLField(max_length=1024)
    mime_type = models.CharField(max_length=255)
    body = models.TextField()
    date = models.DateTimeField()

    class Meta:
        ordering = ('-date', )

    def __unicode__(self):
        return self.link
