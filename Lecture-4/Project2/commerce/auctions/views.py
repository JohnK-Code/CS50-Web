from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import NewListingForm

from .models import User, Listing, Bid, Comment


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all().order_by('startTime'),
        "bids": Bid.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required(login_url="login")
def newlisting(request):
    if request.method == "POST":
        # Get form data
        category = request.POST['category']
        title = request.POST['title']
        make = request.POST['make']
        model = request.POST['model']
        year = request.POST['year']
        description = request.POST['description']
        startBid = request.POST['startBid']
        user = request.user.id
        image = request.FILES.get('images', None) # used to get files from request or provide default

        # create listing
        try:
            listing = Listing(category=category, title=title, make=make, model=model, year=year, description=description, startingBid=startBid, user_id=user, image=image)
            listing.save()
        except IntegrityError as e:
            return render(request, "auctions/newlisting.html", {
                "message": e,
                "form": NewListingForm
            })
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, 'auctions/newlisting.html', {
        'form': NewListingForm
        })