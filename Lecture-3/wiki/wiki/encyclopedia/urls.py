from django.urls import path

from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:page>", views.pages, name="page"),
    path('search', views.search, name="search"),
    path('newpage', views.newpage, name="newpage"),
    path('wiki/<str:page>/edit', views.edit, name="edit")
]
