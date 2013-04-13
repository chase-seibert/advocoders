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
    date_added = models.DateTimeField(auto_now_add=True)
    # branding options
    _branding_enabled = models.BooleanField(default=False,
        verbose_name='Enable Custom Branding')
    backsplash = models.URLField(blank=True,
        verbose_name='Background image URL')
    background_color = RGBColorField(blank=True, default='#FFFFFF')
    link_color = RGBColorField(blank=True, default='#0080c0')
    dark_theme = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name or self.domain

    @property
    def users(self):
        return User.objects.filter(profile__company=self)

    @property
    def branding_enabled(self):
        return settings.BRANDING_ENABLED and self._branding_enabled

    def _color_variant(self, color, intensity):
        from advocoders.utils import color_variant
        if self.dark_theme:
            intensity = -1 * intensity
        return color_variant(color, intensity)

    @property
    def background_color1(self):
        return self._color_variant(self.background_color, -20)

    @property
    def background_color2(self):
        return self._color_variant(self.background_color, -60)

    @property
    def white_or_black(self):
        return 'black' if self.dark_theme else 'white'


class Profile(models.Model):
    user = models.OneToOneField(User)
    company = models.ForeignKey(Company, null=True, verbose_name='Company you want to associate with')
    picture = models.ForeignKey(UserSocialAuth, null=True, verbose_name='Picture you want to use')
    title = models.CharField(max_length=255, blank=True, verbose_name="Your job title")
    blog = models.URLField(null=True, blank=True, verbose_name='Hook up your personal blog to display recent posts in your company feed.')
    picture_override = models.URLField(null=True, blank=True, verbose_name='Admin picture override')
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
        if self.picture_override:
            picture = self.picture_override
        else:
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

    @staticmethod
    def for_company(company, provider=None):
        content_list = Content.objects.filter(user__profile__company=company)
        if provider:
            content_list = content_list.filter(provider=provider)
        else:
            content_list = content_list.exclude(provider='github')
        return content_list
