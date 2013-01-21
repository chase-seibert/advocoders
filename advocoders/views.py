from django.shortcuts import render
from django.contrib.auth import logout as django_logout
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from advocoders.models import Profile
from advocoders.forms import ProfileForm


def home(request):
    return render(request, 'home.html', locals())


def signup(request):
    return render(request, 'signup.html', locals())


@login_required
def profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    form = ProfileForm(instance=profile, user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been saved.')
            return HttpResponseRedirect(reverse('profile'))
    return render(request, 'profile.html', locals())


@login_required
def logout(request):
    django_logout(request)
    messages.success(request, 'You have been logged out.')
    return HttpResponseRedirect(reverse('home'))
