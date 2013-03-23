from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from advocoders.models import Company
from advocoders.models import Content


class CompanyContentFeed(Feed):

    def get_object(self, request, domain, provider=None):
        self.provider = provider
        return get_object_or_404(Company, domain=domain)

    def title(self, company):
        return '%s Engineering Blog' % company

    def link(self, company):
        return reverse('feed_company', args=[company.domain])

    def description(self, company):
        return company.description

    def items(self, company):
        return Content.for_company(company, self.provider)

    def item_title(self, content):
        return content.title

    def item_description(self, content):
        return content.body

    def item_link(self, content):
        return content.link

    def item_pubdate(self, content):
        return content.date

    def item_author_name(self, content):
        return content.user.profile

    def item_author_email(self, content):
        return content.user.email

    def item_author_link(self, content):
        return content.user.profile.blog_url
