from core.shared.models import BaseModel
from django.db import models


class Link(BaseModel):
    title = models.CharField('Título', max_length=255)
    short_link = models.CharField('Link encurtado')
    redirect_to = models.URLField('Redirecionar para')
    clicks = models.IntegerField('Cliques', default=0)

    class Meta:
        ordering = ['title']
        verbose_name = 'Link'
        verbose_name_plural = 'Links'
    
    def __str__(self):
        return self.title
