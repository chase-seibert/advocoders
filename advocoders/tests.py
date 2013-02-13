import unittest
from advocoders.utils import sanitize_html
from advocoders.utils import santize_and_hightlight_html


class HtmlSanitiztionTests(unittest.TestCase):

    def test_script(self):
        self.assertEquals(sanitize_html('foobar<script src="//hack.me/danger.js">'), 'foobar')


class HighlightCodeTests(unittest.TestCase):

    def test_pygments(self):
        ''' don't re-encode it if it's already in the right format '''
        self.assertEquals(santize_and_hightlight_html(
            u'<div class="highlight"><pre><code class="python"><span class="kn">import</span><span class="nn">urllib2</span></code></pre></div>'),
            u'<div class="highlight"><pre><code class="python"><span class="kn">import</span><span class="nn">urllib2</span></code></pre></div>')

    def test_pre(self):
        self.assertEquals(santize_and_hightlight_html(
            u'<pre>foobar</pre>'),
            u'<div class="highlight"><pre><span class="n">foobar</span></pre></div>')

    def test_stackoverflow(self):
        self.assertEquals(santize_and_hightlight_html(provider='stackoverflow', html=
            u'<pre><code>foobar</code></pre>'),
            u'<div class="highlight"><pre><span class="n">foobar</span></pre></div>')


if __name__ == '__main__':
    unittest.main()
