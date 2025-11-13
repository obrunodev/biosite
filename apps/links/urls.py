from django.urls import path
from apps.links import views

app_name = 'links'
urlpatterns = [
    path('', views.LinkListView.as_view(), name='list'),
    path('<str:short_link>/', views.redirect_to, name='redirect_to'),
]
