from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import NewListingForm

from .models import User, Listing, Bid, Comment, categories
from decimal import Decimal


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all().order_by('-startTime'),
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
        # Access form data
        category = request.POST['category']
        title = request.POST['title']
        make = request.POST['make']
        model = request.POST['model']
        year = request.POST['year']
        description = request.POST['description']
        startBid = request.POST['startBid']
        user = request.user.id
        image = request.FILES.get('image', None) # used to get files from request or provide default

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

def listing(request, id):
    if not request.user.is_authenticated:
        return render(request, "auctions/listing.html", {
            "advert": Listing.objects.get(id=id)    
        })
    else:
        listing = Listing.objects.get(id=id)
        if listing.bid_listing.exists():
            is_watch_list = request.user.watchlist.filter(pk=id)
            return render(request, "auctions/listing.html", {
                "advert": listing,
                "current_user": request.user.id,
                'is_watch_list': is_watch_list,
                'price': listing.bid_listing.last().currentBid + 50,
                'commentList': listing.comment_listing.all().order_by('-commentTime')  #############################
            })
        else:
            is_watch_list = request.user.watchlist.filter(pk=id)
            return render(request, "auctions/listing.html", {
                "advert": listing,
                "current_user": request.user.id,
                'is_watch_list': is_watch_list,
                'price': listing.startingBid + 50,
                'commentList': listing.comment_listing.all().order_by('-commentTime')
            })


@login_required
def watchlistedit(request, id):
    if request.method == "POST":
        user = request.user
        listing = Listing.objects.get(pk=id)
        if user.watchlist.filter(pk=id).exists():
            user.watchlist.remove(listing)
        else:
            user.watchlist.add(listing)
        
    return HttpResponseRedirect(reverse("listing", args=(id,)))

@login_required
def newbid(request, id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=id)
        bid = Decimal(request.POST['bid'])
        biduser = request.user

        if Bid.objects.filter(listing=listing):
            oldprice = listing.bid_listing.last().currentBid
            if  bid > oldprice:
                newbid = Bid(listing=listing, currentBid=bid, bidder=biduser)
                newbid.save()
                return HttpResponseRedirect(reverse("listing", args=(id,)))
            else:
                return render(request, "auctions/listing.html", {
                "advert": Listing.objects.get(id=id),
                "current_user": request.user.id,
                'is_watch_list': request.user.watchlist.filter(pk=id),
                "low": "Please, enter a bid higher than the Current Price!",
                "price": listing.bid_listing.last().currentBid + 10,
                'commentList': listing.comment_listing.all().order_by('-commentTime')
                })
        else:
            if bid > listing.startingBid:
                newbid = Bid(listing=listing, currentBid=bid, bidder=biduser)
                newbid.save()
                return HttpResponseRedirect(reverse("listing", args=(id,)))
            else:
                return render(request, "auctions/listing.html", {
                "advert": Listing.objects.get(id=id),
                "current_user": request.user.id,
                'is_watch_list': request.user.watchlist.filter(pk=id),
                "low": "Please, enter a bid higher than the Current Price!",
                "price": listing.startingBid + 10,
                'commentList': listing.comment_listing.all().order_by('-commentTime')
                })


@login_required
def activeadvert(request, id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=id)
        if listing.active:
            listing.active = False
            listing.save()
            return HttpResponseRedirect(reverse("listing", args=(id,)))
        else:
            listing.active = True
            listing.save()
            return HttpResponseRedirect(reverse('listing', args=(id,)))


@login_required
def comment(request, id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=id)
        commentNew = request.POST["comment"]
        commentuser = request.user

        newComment = Comment(comment=commentNew, user=commentuser, listing=listing)
        newComment.save()
        return HttpResponseRedirect(reverse('listing', args=(id,)))

@login_required
def watchlist(request):
    user = request.user
    return render(request, "auctions/watchlist.html", {
        "userlist": user.watchlist.all()
    })

def category(request):
    categoryList = []
    for item in categories:
        categoryList.append(item[0]) 
    return render(request, "auctions/categories.html", {
        'categories': categoryList
    })

def categoryList(request, category):
    if request.method == "POST":
        listings = Listing.objects.filter(category=category)
        return render(request, "auctions/categoryList.html", {
            "listings": listings
        })

def delete(request, id):
    if request.method == "POST":
        advert = Listing.objects.get(pk=id)
        advert.delete()
    return HttpResponseRedirect(reverse('index'))