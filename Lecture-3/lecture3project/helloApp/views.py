from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request): # creates a view using the render function and django templates
    return render(request, "hello/index.html")

def brian(request): # creates view using Http response - what will be displayed to user when url (url.py) entered in browser that is a associated with this view
    return HttpResponse("Hello, Brian!")

def david(request):
    return HttpResponse("Hello, David!")

def greet(request, name): # creates a view that accepts a paramater that has been entered into the url (name) as part of the urls.py file
    return render(request, "hello/greet.html", { # uses render function and allows parameters that can be passed the the html file to be rendered
        "name": name.capitalize()
    })
