import re
import feedparser
from dateutil.parser import parse as dateutil_parse
from BeautifulSoup import BeautifulSoup
import pygments
import pygments.formatters
import pygments.lexers
import bleach
from advocoders.models import Content
from advocoders.models import Profile


def update_feeds(*args, **kwargs):
    for profile in Profile.objects.all():
        for provider, rss_url in profile.rss_urls:
            try:
                update_feed(profile, provider, rss_url)
            except Exception, e:
                print e


def update_feed(profile, provider, rss_url):

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
        content.mime_type, content.body = get_body_and_mime_type(entry)
        if content.mime_type == 'text/html':
            content.body = santize_and_hightlight_html(content.body)
        content.save()


def get_body_and_mime_type(entry):
    try:
        return entry.content[0].type, entry.content[0].value
    except AttributeError:
        return 'text/html', entry.summary


def get_domain(email):
    return email.split('@')[1]


def pre_process(html):
    ''' replace whitelisted html w/ tokens '''
    html = re.sub('<script src=.http.://gist.github.com/([0-9]+).js.></script>',
        'ADVO_GIST:\\1', html)
    return html


def post_process(html):
    ''' replace whitelisted tokens w/ safe html '''
    html = re.sub('ADVO_GIST:([0-9]+)',
        '<script src="//gist.github.com/\\1.js"></script>', html)
    return html


def santize_and_hightlight_html(html, provider=None):
    klass = 'pre'  # may need to do something different per provider
    html = pre_process(html)
    html = sanitize_html(html)
    html = highlight_code_inside_html(html, klass)
    html = post_process(html)
    return html


def sanitize_html(html):
    return bleach.clean(
        html,
        tags=bleach.ALLOWED_TAGS + ['p', 'pre', 'div', 'span', 'br', 'table', 'tr', 'td',
            'tbody', 'thead', 'a', 'blockquote', 'ul', 'li', 'ol', 'b', 'em', 'i',
            'strong', 'u', 'font'],
        attributes=['a', 'class'],
        strip=True)


def highlight_code_inside_html(html, klass='pre'):
    ''' from: http://stefan.sofa-rockers.org/2010/01/13/django-highlighting-html-using-pygments-and-beauti '''
    soup = BeautifulSoup(html)
    highlighted_already = soup.findAll('div', 'highlight')
    if highlighted_already:
        return html
    codeblocks = soup.findAll(klass)
    for block in codeblocks:
        try:
            code = ''.join(block.findAll(text=True))
            lexer = pygments.lexers.guess_lexer(code)
            formatter = pygments.formatters.HtmlFormatter()
            code_hl = pygments.highlight(code, lexer, formatter)
            block.replaceWith(BeautifulSoup(code_hl))
        except Exception, e:
            print 'Exception in highlight_code_inside_html: %s' % e
    return unicode(soup)
