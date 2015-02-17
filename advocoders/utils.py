import re
import feedparser
from dateutil.parser import parse as dateutil_parse
from BeautifulSoup import BeautifulSoup
import pygments
import pygments.formatters
import pygments.lexers
import bleach
import HTMLParser
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
        content.date = dateutil_parse(getattr(entry, 'published', entry.updated))
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
    html = re.sub('<script src=.http.?://gist.github.com/([0-9]+).js.></script>',
        'ADVO_GIST:\\1', html)
    html = re.sub('<a href=.http.?://gist.github.com/([0-9]+).>http.?://gist.github.com/[0-9]+</a>',
        'ADVO_GIST:\\1', html)
    _htmlparser = HTMLParser.HTMLParser()
    html = _htmlparser.unescape(html)
    return html


def post_process(html):
    ''' replace whitelisted tokens w/ safe html '''
    html = re.sub('ADVO_GIST:([0-9]+)',
        '<script src="//gist.github.com/\\1.js"></script>', html)
    html = re.sub('<p style=..>&nbsp;</p>', '', html)
    html = re.sub('<p style="">\xa0</p>', '', html)
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
        tags=bleach.ALLOWED_TAGS + ['img', 'p', 'pre', 'div', 'span', 'br', 'table', 'tr', 'td',
            'tbody', 'thead', 'th', 'a', 'blockquote', 'ul', 'li', 'ol', 'b', 'em', 'i',
            'strong', 'u', 'font'],
        attributes=['a', 'class', 'href', 'color', 'size', 'bgcolor', 'border', 'style', ],
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
            _htmlparser = HTMLParser.HTMLParser()
            code = _htmlparser.unescape(code)
            lexer = pygments.lexers.guess_lexer(code)
            formatter = pygments.formatters.HtmlFormatter()
            code_hl = pygments.highlight(code, lexer, formatter)
            block.replaceWith(BeautifulSoup(code_hl))
        except Exception, e:
            print 'Exception in highlight_code_inside_html: %s' % e
    return unicode(soup)


def canonical_social_auth(provider):
    if provider == "google-oauth2":
        return "Google Apps"
    if provider == "github":
        return "GitHub"
    if provider == "stackoverflow":
        return "Stack Overflow"
    return provider


# from: http://chase-seibert.github.com/blog/2011/07/29/python-calculate-lighterdarker-rgb-colors.html
def color_variant(hex_color, brightness_offset=1):
    """ takes a color like #87c95f and produces a lighter or darker variant """
    if len(hex_color) != 7:
        raise Exception("Passed %s into color_variant(), needs to be in #87c95f format." % hex_color)
    rgb_hex = [hex_color[x: x + 2] for x in [1, 3, 5]]
    new_rgb_int = [int(hex_value, 16) + brightness_offset for hex_value in rgb_hex]
    new_rgb_int = [min([255, max([0, i])]) for i in new_rgb_int]  # make sure new values are between 0 and 255
    # hex() produces "0x88", we want just "88"
    return "#" + "".join([hex(i)[2:] for i in new_rgb_int])
