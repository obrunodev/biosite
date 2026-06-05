from apps.links.forms import BioPageSlugForm, LinkForm, RegisterForm, suggest_slug
from apps.links.models import BioPage, Link


def get_or_create_bio_page(user):
    bio_page, _ = BioPage.objects.get_or_create(
        user=user,
        defaults={'slug': suggest_slug(user.username)},
    )
    return bio_page

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView, View


class UserLoginView(LoginView):
    template_name = 'links/login.html'
    redirect_authenticated_user = True


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('links:login')


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'links/register.html'
    success_url = reverse_lazy('links:manage')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('links:manage')
        return super().dispatch(request, *args, **kwargs)

    @transaction.atomic
    def form_valid(self, form):
        user = form.save()
        BioPage.objects.create(user=user, slug=form.cleaned_data['slug'])
        login(self.request, user)
        messages.success(self.request, 'Conta criada com sucesso!')
        return redirect(self.success_url)


class LinkManageListView(LoginRequiredMixin, ListView):
    model = Link
    template_name = 'links/manage_list.html'
    context_object_name = 'links'

    def get_queryset(self):
        return Link.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bio_page'] = get_or_create_bio_page(self.request.user)
        return context


class BioPageSlugUpdateView(LoginRequiredMixin, UpdateView):
    model = BioPage
    form_class = BioPageSlugForm
    template_name = 'links/bio_slug_form.html'

    def get_object(self):
        return get_or_create_bio_page(self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Slug atualizado com sucesso!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('links:manage')


class LinkCreateView(LoginRequiredMixin, CreateView):
    model = Link
    form_class = LinkForm
    template_name = 'links/link_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Link criado com sucesso!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('links:manage')


class LinkUpdateView(LoginRequiredMixin, UpdateView):
    model = Link
    form_class = LinkForm
    template_name = 'links/link_form.html'

    def get_queryset(self):
        return Link.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Link atualizado com sucesso!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('links:manage')


class LinkDeleteView(LoginRequiredMixin, DeleteView):
    model = Link
    template_name = 'links/link_confirm_delete.html'

    def get_queryset(self):
        return Link.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Link removido com sucesso!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('links:manage')


class LinkToggleActiveView(LoginRequiredMixin, View):
    def post(self, request, pk):
        link = get_object_or_404(Link, pk=pk, user=request.user)
        link.is_active = not link.is_active
        link.save(update_fields=['is_active', 'updated_at'])
        status = 'ativado' if link.is_active else 'desativado'
        messages.success(request, f'Link {status} com sucesso!')
        return redirect('links:manage')


def slug_or_redirect(request, slug):
    link = Link.objects.filter(short_link=slug, is_active=True).first()
    if link:
        Link.objects.filter(pk=link.pk).update(clicks=F('clicks') + 1)
        link.refresh_from_db()
        return redirect(link.redirect_to)

    bio_page = get_object_or_404(BioPage, slug=slug)
    links = Link.objects.filter(user=bio_page.user, is_active=True)
    return render(request, 'links/link_list.html', {
        'links': links,
        'bio_page': bio_page,
    })
