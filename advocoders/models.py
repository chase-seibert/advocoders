from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from social_auth.models import UserSocialAuth
from colorful.fields import RGBColorField


class Company(models.Model):
    domain = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, blank=True)
    website_url = models.URLField(blank=True)
    logo = models.URLField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    backsplash = models.URLField(blank=True)
    background_color = RGBColorField(blank=True)
    link_color = RGBColorField(blank=True)
    dark_theme = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name or self.domain

    @property
    def users(self):
        return User.objects.filter(profile__company=self)


class Profile(models.Model):
    user = models.OneToOneField(User)
    company = models.ForeignKey(Company, null=True, verbose_name='Company you want to associate with')
    picture = models.ForeignKey(UserSocialAuth, null=True, verbose_name='Picture you want to use')
    title = models.CharField(max_length=255, blank=True, verbose_name="Your job title")
    blog = models.URLField(verbose_name='Hook up your personal blog to display recent posts in your company feed.')
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
        for social_auth in self.user.social_auth.all():
            rss_url = social_auth.extra_data.get('rss_url')
            if rss_url:
                yield (social_auth.provider, rss_url)

    @property
    def picture_url(self):
        picture = self.picture.extra_data.get('picture') if self.picture else None
        return picture or '/static/images/generic-headshot-male.jpg'

    @property
    def full_name(self):
        name = ('%s %s' % (self.user.first_name, self.user.last_name)).strip()
        return name or self.user

    @property
    def blog_url(self):
        if not self.blog:
            return ''
        return '/'.join(self.blog.split('/')[:-1])

    def save(self, *args, **kwargs):
        current = None
        if hasattr(self, 'id') and self.id:
            current = Profile.objects.get(pk=self.id)
        super(Profile, self).save(*args, **kwargs)
        if current and current.blog != self.blog:
            from advocoders import tasks
            tasks.update_feed.delay(self.id, 'blog')


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
