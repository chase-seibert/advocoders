from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe
from advocoders.models import Profile
from advocoders.models import Company
from advocoders import utils


def headshot_label(auth):
    return mark_safe('<img src="%s" class="fixed-width img-polaroid"> %s' % (
        auth.extra_data.get('picture', ''),
        utils.canonical_social_auth(auth.provider)))


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'title', 'picture', )

    first_name = forms.CharField()
    last_name = forms.CharField()

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['picture'].choices = [(auth.id, headshot_label(auth))
            for auth in self.user.social_auth.all()]
        self.fields['picture'].widget = forms.widgets.RadioSelect()
        self.fields['first_name'].initial = self.user.first_name
        self.fields['last_name'].initial = self.user.last_name

    def save(self, *args, **kwargs):
        super(ProfileForm, self).save(*args, **kwargs)
        self.user.first_name = self.cleaned_data.get('first_name')
        self.user.last_name = self.cleaned_data.get('last_name')
        self.user.save()


class CompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        _branding_fields = ('_branding_enabled', 'backsplash', 'background_color',
            'link_color', 'dark_theme', )
        fields = ('name', 'website_url', 'logo', 'location', 'description', )

        def __init__(self, *args, **kwargs):
            if not settings.BRANDING_ENABLED:
                for field in self._branding_fields:
                    self.fields[field].enabled = False
            return super(CompanyForm, self).__init__(*args, **kwargs)


class BlogForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('blog', )
