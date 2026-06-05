from apps.links import views

from django.urls import path
from django.views.generic import RedirectView

app_name = 'links'
urlpatterns = [
    path('', RedirectView.as_view(pattern_name='links:login', permanent=False)),
    path('bio/', views.LinkManageListView.as_view(), name='manage'),
    path('bio/slug/', views.BioPageSlugUpdateView.as_view(), name='bio_slug'),
    path('bio/novo/', views.LinkCreateView.as_view(), name='create'),
    path('bio/<int:pk>/editar/', views.LinkUpdateView.as_view(), name='update'),
    path('bio/<int:pk>/excluir/', views.LinkDeleteView.as_view(), name='delete'),
    path('bio/<int:pk>/desativar/', views.LinkToggleActiveView.as_view(), name='toggle_active'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('registro/', views.RegisterView.as_view(), name='register'),
    path('<slug:slug>/', views.slug_or_redirect, name='slug_or_redirect'),
]
