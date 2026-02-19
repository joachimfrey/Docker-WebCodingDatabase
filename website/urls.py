from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("liste", views.liste, name="liste"),
    path("liste_edit", views.liste_edit, name="liste_edit" ),
    path('skripte', views.skripte, name='skripte'),
    path('roadmap', views.roadmap, name='roadmap')
]