from django.shortcuts import render
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.template import defaultfilters
from advocoders.forms import ProfileForm
from advocoders.forms import BlogForm
from advocoders.forms import CompanyForm
from advocoders.models import Company
from advocoders.models import Content


def home(request, domain=None, provider=None):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('feed_company', args=[request.company.domain]))
    recent_companies = Company.objects.filter(profile__user__content__isnull=False).distinct()[:5]
    recent_users = User.objects.filter(profile__picture__isnull=False)[:5]
    return render(request, 'home.html', locals())


def feed(request, domain=None, provider=None):
    content_list = Content.objects.all()
    if domain:
        company = get_object_or_404(Company, domain=domain)
        content_list = content_list.filter(user__profile__company=company)
    if provider:
        content_list = content_list.filter(provider=provider)
    else:
        content_list = content_list.exclude(provider='github')
    page = request.GET.get('page', 1)
    paginator = Paginator(content_list, 10)
    content_list = paginator.page(page)
    return render(request, 'feed.html', locals())


@login_required
def settings_profile(request):
    form = ProfileForm(instance=request.profile, user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been saved.')
            return HttpResponseRedirect(reverse('settings_feeds') + '?initial=True'
                if request.REQUEST.get('initial') else reverse('settings_profile'))
    return render(request, 'settings/profile.html', locals())


@login_required
def settings_feeds(request):
    next_url = reverse('settings_feeds')
    if request.REQUEST.get('initial'):
        next_url = next_url + defaultfilters.urlencode('?initial=True')
    form = BlogForm(instance=request.profile)
    if request.method == 'POST':
        form = BlogForm(request.POST, instance=request.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been saved.')
    return render(request, 'settings/feeds.html', locals())


@login_required
def settings_company(request):
    form = CompanyForm(instance=request.company)
    if request.method == 'POST':
        form = CompanyForm(request.POST, instance=request.company)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your company information has been updated')
            return HttpResponseRedirect(reverse('my_company')
                if request.REQUEST.get('initial') else reverse('settings_company'))
    other_users = request.company.profile_set.all().exclude(user=request.profile)
    return render(request, 'settings/company.html', locals())


@login_required
def my_company(request):
    return HttpResponseRedirect(reverse('feed_company', args=[request.company.domain]))


@login_required
def logout(request):
    django_logout(request)
    messages.success(request, 'You have been logged out.')
    return HttpResponseRedirect(reverse('home'))
