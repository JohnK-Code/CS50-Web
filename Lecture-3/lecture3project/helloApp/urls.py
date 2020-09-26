from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"), # used to access the index view in helloApp views.py file
    path("brian", views.brian, name="brian"), # used to access the brian view in helloApp views.py file
    path("david", views.david, name="david"), # used to access the david view in helloApp views.py file
    path("<str:name>", views.greet, name="greet") # allows acces to the greet view using any string in the url
]