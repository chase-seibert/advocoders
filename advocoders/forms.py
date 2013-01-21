from django import forms
from advocoders.models import Profile


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('company', 'picture', 'title', 'blog',)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['company'].choices = [(company.id, company.domain) for company in self.user.profile.company_choices]
        self.fields['picture'].choices = [(auth.id, auth.provider) for auth in self.user.social_auth.all()]
        self.fields['blog'].required = False
