import unittest
from advocoders.utils import sanitize_html
from advocoders.utils import santize_and_hightlight_html


class HtmlSanitiztionTests(unittest.TestCase):

    def test_script(self):
        self.assertEquals(sanitize_html('foobar<script src="//hack.me/danger.js">'), 'foobar')

    def test_html_decode_aleady(self):
        self.assertEquals(santize_and_hightlight_html('<p>foobar</p>'),
            '<p>foobar</p>')

    def test_empty_paragraphs(self):
        self.assertEquals(santize_and_hightlight_html('<p style="margin: 0px; font-family: Times New Roman; font-size: medium;">&nbsp;</p>'),
            '')


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
        self.assertEquals(santize_and_hightlight_html(
            u'<a href="https://gist.github.com/2635479">https://gist.github.com/2635479</a>'),
            u'<script src="//gist.github.com/2635479.js"></script>')

    def test_newlines(self):
        self.assertEquals(santize_and_hightlight_html(
            u'<pre>foobar\nfoobar</pre>'),
            u'<div class="highlight"><pre><span class="n">foobar</span>\n<span class="n">foobar</span>\n</pre></div>\n')

    def test_pre_encoded(self):
        self.assertEquals(santize_and_hightlight_html(
            u'<div class="code"><pre>&gt;&gt;&gt; print type("%s" % a)&lt;type \'str\'&gt; &lt;type \'unicode\'&gt;</pre></div>'),
            u'<div class="code"><div class="highlight"><pre><span class="o">&gt;&gt;&gt;</span> <span class="n">print</span> <span class="n">type</span><span class="p">(</span><span class="s">&quot;%s&quot;</span> <span class="o">%</span> <span class="n">a</span><span class="p">)</span> \n</pre></div>\n</div>')


if __name__ == '__main__':
    unittest.main()
