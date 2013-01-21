import feedparser
from dateutil.parser import parse as dateutil_parse
from advocoders.models import Content
from advocoders.models import Profile


def update_feeds(*args, **kwargs):
    for profile in Profile.objects.all():
        for provider, rss_url in profile.rss_urls:

            Content.objects.filter(
                user=profile.user,
                provider=provider).delete()

            print rss_url
            feed = feedparser.parse(rss_url)
            for entry in feed.get('entries')[:10]:
                content = Content()
                content.user = profile.user
                content.provider = provider
                content.title = entry.title
                content.link = entry.link
                content.date = dateutil_parse(entry.updated)
                content.mime_type = entry.content[0].type
                content.body = entry.content[0].value
                content.save()


def get_domain(email):
    return email.split('@')[1]
