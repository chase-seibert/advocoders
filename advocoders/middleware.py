from django.core.urlresolvers import resolve
from advocoders.models import Company
from advocoders.models import Profile
from advocoders import utils


class ViewNameMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        url_name = resolve(request.path).url_name
        request.current_view = url_name


class DefaultRequestVars(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        request.current_url = request.build_absolute_uri()
        if request.user.is_authenticated():
            company, _ = Company.objects.get_or_create(domain=utils.get_domain(request.user.email))
            profile, created = Profile.objects.get_or_create(user=request.user)
            if created or not profile.company:
                profile.company = company
                profile.save()
            request.company, request.profile = company, profile
