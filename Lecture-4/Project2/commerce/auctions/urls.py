from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

#app_name = 'auctions'
urlpatterns = [
    path("", views.index, name="index"),
    path("Login", views.login_view, name="login"),
    path("Logout", views.logout_view, name="logout"),
    path("Register", views.register, name="register"),
    path("Newlisting", views.newlisting, name="newlisting"),
    path("Listing/<int:id>", views.listing, name="listing"), # image works if i remove listing/ from path
    path("Watchlist/<int:id>", views.watchlistedit, name="watchlistedit"),
    path("Bid/<int:id>", views.newbid, name="bid"),
    path("Active/<int:id>", views.activeadvert, name="active"),
    path("Comment/<int:id>", views.comment, name="addcomment"),
    path("Watch", views.watchlist, name="watchlist"),
    path("Categories", views.category, name="categories"),
    path("Categories/<str:category>", views.categoryList, name="categoryList"),
    path("delete/<int:id>", views.delete, name="delete")
]