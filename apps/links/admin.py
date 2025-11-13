from apps.links.models import Link

from django.contrib import admin


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ['title', 'clicks']
