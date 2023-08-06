from django.contrib import admin

from apps.accounts.models import Site, Membership

class SiteModelAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "slug", "share", "created_by")

    class Meta:
        model = Site


admin.site.register(Site, SiteModelAdmin)

class MembershipModelAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "host", "rights")

    class Meta:
        model = Site


admin.site.register(Membership, MembershipModelAdmin)

