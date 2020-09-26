"""lecture3project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', include("helloApp.urls")), # add hello path provides access to all urls in the helloApp app - added by John
    path("newyear/", include("newyear.urls")), # provide access to all urls in the newyear app
    path("tasks/", include("tasks.urls")) # gives the project acces to all urls in the tasks app at the (127.0.0.1/tasks/) url
]
