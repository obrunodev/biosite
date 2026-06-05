from core.shared.models import BaseModel
from django.conf import settings
from django.db import models


RESERVED_SLUGS = {'bio', 'login', 'logout', 'registro', 'admin'}


class BioPage(BaseModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bio_page',
        verbose_name='Usuário',
    )
    slug = models.SlugField('Slug da bio', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Página bio'
        verbose_name_plural = 'Páginas bio'

    def __str__(self):
        return self.slug


class Link(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='links',
        verbose_name='Usuário',
    )
    title = models.CharField('Título', max_length=255)
    short_link = models.SlugField('Link encurtado', max_length=50, unique=True)
    redirect_to = models.URLField('Redirecionar para')
    clicks = models.IntegerField('Cliques', default=0)
    is_active = models.BooleanField('Ativo', default=True)

    class Meta:
        ordering = ['title']
        verbose_name = 'Link'
        verbose_name_plural = 'Links'

    def __str__(self):
        return self.title
