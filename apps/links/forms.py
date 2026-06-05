from apps.links.models import BioPage, Link, RESERVED_SLUGS

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.text import slugify


def suggest_slug(username):
    base = slugify(username) or 'usuario'
    slug = base
    counter = 1
    while BioPage.objects.filter(slug=slug).exists():
        slug = f'{base}-{counter}'
        counter += 1
    return slug


class RegisterForm(UserCreationForm):
    slug = forms.SlugField(
        label='Slug da sua bio',
        max_length=50,
        help_text='URL pública da sua página. Ex: meusite.com/seu-slug',
    )

    class Meta:
        model = User
        fields = ('username', 'slug')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.initial.get('username') and 'slug' not in self.data:
            self.fields['slug'].initial = suggest_slug(self.initial['username'])

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('slug') and cleaned_data.get('username'):
            cleaned_data['slug'] = suggest_slug(cleaned_data['username'])
        return cleaned_data

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        if slug in RESERVED_SLUGS:
            raise forms.ValidationError('Este slug é reservado pelo sistema.')
        if BioPage.objects.filter(slug=slug).exists():
            raise forms.ValidationError('Este slug já está em uso.')
        if Link.objects.filter(short_link=slug).exists():
            raise forms.ValidationError('Este slug conflita com um link encurtado existente.')
        return slug


class BioPageSlugForm(forms.ModelForm):
    class Meta:
        model = BioPage
        fields = ('slug',)
        labels = {'slug': 'Slug da sua bio'}

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        if slug in RESERVED_SLUGS:
            raise forms.ValidationError('Este slug é reservado pelo sistema.')
        if (
            BioPage.objects.filter(slug=slug)
            .exclude(pk=self.instance.pk)
            .exists()
        ):
            raise forms.ValidationError('Este slug já está em uso.')
        if Link.objects.filter(short_link=slug).exists():
            raise forms.ValidationError('Este slug conflita com um link encurtado existente.')
        return slug


class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ('title', 'short_link', 'redirect_to', 'is_active')
        labels = {
            'title': 'Título',
            'short_link': 'Link encurtado',
            'redirect_to': 'Redirecionar para',
            'is_active': 'Ativo',
        }

    def clean_short_link(self):
        short_link = self.cleaned_data['short_link']
        if short_link in RESERVED_SLUGS:
            raise forms.ValidationError('Este slug é reservado pelo sistema.')
        if BioPage.objects.filter(slug=short_link).exists():
            raise forms.ValidationError('Este slug conflita com uma página bio existente.')
        qs = Link.objects.filter(short_link=short_link)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('Este link encurtado já está em uso.')
        return short_link
