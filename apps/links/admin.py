from apps.links.models import BioPage, Link

from django.contrib import admin


@admin.register(BioPage)
class BioPageAdmin(admin.ModelAdmin):
    list_display = ['slug', 'user']
    search_fields = ['slug', 'user__username']


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'short_link', 'clicks', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'short_link', 'user__username']
