import unittest
from advocoders.utils import sanitize_html
from advocoders.utils import santize_and_hightlight_html


class HtmlSanitiztionTests(unittest.TestCase):

    def test_script(self):
        self.assertEquals(sanitize_html('foobar<script src="//hack.me/danger.js">'), 'foobar')

    def test_html_decode(self):
        self.assertEquals(santize_and_hightlight_html('&lt;'),
            '<')

    def test_html_decode_aleady(self):
        self.assertEquals(santize_and_hightlight_html('<p>foobar</p>'),
            '<p>foobar</p>')


class HighlightCodeTests(unittest.TestCase):

    def test_pygments(self):
        ''' don't re-encode it if it's already in the right format '''
        self.assertEquals(santize_and_hightlight_html(
            u'<div class="highlight"><pre><code class="python"><span class="kn">import</span><span class="nn">urllib2</span></code></pre></div>'),
            u'<div class="highlight"><pre><code class="python"><span class="kn">import</span><span class="nn">urllib2</span></code></pre></div>')

    def test_pre(self):
        self.assertEquals(santize_and_hightlight_html(
            u'<pre>foobar</pre>'),
            u'<div class="highlight"><pre><span class="n">foobar</span>\n</pre></div>\n')

    def test_stackoverflow(self):
        self.assertEquals(santize_and_hightlight_html(provider='stackoverflow', html=
            u'<pre><code>foobar</code></pre>'),
            u'<div class="highlight"><pre><span class="n">foobar</span>\n</pre></div>\n')

    def test_posterous(self):
        self.assertEquals(santize_and_hightlight_html(
            u'<div class="code"><pre>foobar</pre></div>'),
            u'<div class="code"><div class="highlight"><pre><span class="n">foobar</span>\n</pre></div>\n</div>')

    def test_gist(self):
        ''' scripts from this domain alone should be allowed '''
        self.assertEquals(santize_and_hightlight_html(
            u'<script src="https://gist.github.com/2635479.js"></script>'),
            u'<script src="//gist.github.com/2635479.js"></script>')

    def test_newlines(self):
        self.assertEquals(santize_and_hightlight_html(
            u'<pre>foobar\nfoobar</pre>'),
            u'<div class="highlight"><pre><span class="n">foobar</span>\n<span class="n">foobar</span>\n</pre></div>\n')


if __name__ == '__main__':
    unittest.main()
