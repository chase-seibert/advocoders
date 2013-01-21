from django.contrib import admin
from advocoders.models import Company
from advocoders.models import Profile
from advocoders.models import Content


class CompanyAdmin(admin.ModelAdmin):
    pass


admin.site.register(Company, CompanyAdmin)


class ProfileAdmin(admin.ModelAdmin):
    pass


admin.site.register(Profile, ProfileAdmin)


class ContentAdmin(admin.ModelAdmin):
    pass


admin.site.register(Content, ContentAdmin)
