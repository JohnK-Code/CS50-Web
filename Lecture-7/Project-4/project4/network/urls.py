
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.submit_post, name="new_post"),
    path("profile/<int:id>", views.profile_page, name="profile"),
    path("follow/<int:id>", views.follow, name="follow"),
    path("following", views.following, name="following")
]
