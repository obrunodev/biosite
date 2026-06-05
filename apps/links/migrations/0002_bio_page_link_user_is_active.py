import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models
from django.utils.text import slugify


def assign_orphan_links(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    BioPage = apps.get_model('links', 'BioPage')
    Link = apps.get_model('links', 'Link')

    user = User.objects.first()
    if not user:
        return

    base_slug = slugify(user.username) or 'usuario'
    slug = base_slug
    counter = 1
    while BioPage.objects.filter(slug=slug).exists():
        slug = f'{base_slug}-{counter}'
        counter += 1

    BioPage.objects.get_or_create(user=user, defaults={'slug': slug})
    Link.objects.filter(user__isnull=True).update(user=user)


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('links', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BioPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('slug', models.SlugField(max_length=50, unique=True, verbose_name='Slug da bio')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='bio_page', to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'Página bio',
                'verbose_name_plural': 'Páginas bio',
            },
        ),
        migrations.AddField(
            model_name='link',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Ativo'),
        ),
        migrations.AddField(
            model_name='link',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='links', to=settings.AUTH_USER_MODEL, verbose_name='Usuário'),
        ),
        migrations.RunPython(assign_orphan_links, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='link',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='links', to=settings.AUTH_USER_MODEL, verbose_name='Usuário'),
        ),
        migrations.AlterField(
            model_name='link',
            name='short_link',
            field=models.SlugField(max_length=50, unique=True, verbose_name='Link encurtado'),
        ),
    ]
