from django import forms
from advocoders.models import Profile
from advocoders.models import Company


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'picture', 'title', 'blog')

    first_name = forms.CharField()
    last_name = forms.CharField()

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(ProfileForm, self).__init__(*args, **kwargs)
        #self.fields['company'].choices = [(company.id, company.domain) for company in self.user.profile.company_choices]
        self.fields['picture'].choices = [(auth.id, auth.provider) for auth in self.user.social_auth.all()]
        self.fields['blog'].required = False
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
        fields = ('name', 'website_url', 'logo', 'location', 'description')
