from apps.links.models import Link

from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView


class LinkListView(ListView):
    model = Link
    context_object_name = 'links'


def redirect_to(request, short_link):
    link = get_object_or_404(Link, short_link=short_link)
    link.clicks += 1
    link.save()
    return redirect(link.redirect_to)
