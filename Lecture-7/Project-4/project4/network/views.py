from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post, Follower
from .forms import NewPost


def index(request):
    return render(request, "network/index.html", {
        "post_form": NewPost,
        "all_posts": Post.objects.all().order_by('-date_created')
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

# view for submitting New Post
@login_required(login_url=login)
def submit_post(request):
    if request.method == 'POST':
        # get form data from request
        content = request.POST['content']
        author = request.user.id
        
        try:
            post = Post(content=content, author_id=author)
            post.save()
        except IntegrityError as e:
            return render(request, "network/index.html", {
                "message": e,
                "form": NewPost
            })
        return HttpResponseRedirect(reverse("index"))

# view for rendering a user profile page
def profile_page(request, id):
    profile = User.objects.get(id=id)
    if Follower.objects.filter(user=profile).filter(follower=request.user.id):
        being_followed = True
    else:
        being_followed = False

    return render(request, "network/profile.html", {
        "profile": profile,
        "posts": Post.objects.filter(author_id=id).order_by("-date_created"),
        "followers": Follower.objects.filter(user_id=id).count(),
        "following": Follower.objects.filter(follower_id=id).count(),
        "current_user": request.user.id,
        "being_followed": being_followed
    })

# view for updating user followers in database
@login_required(login_url=register)
def follow(request, id):
    if request.method == "POST":
        current_user = request.user
        profile_id = User.objects.get(id=id)
        follow = request.POST['follow']
        if follow == 'follow':
            create_follower = Follower(user=profile_id, follower=current_user)
            create_follower.save()
        elif follow == 'unfollow':
            delete_follower = Follower.objects.filter(user=profile_id, follower=current_user)
            delete_follower.delete()

        return HttpResponseRedirect(reverse("profile", args=(id,)))

# view for displaying posts for all users being followed by current logged in user
@login_required(login_url=register)
def following(request):
    user = User.objects.get(id=request.user.id)
    following = user.followers.all()
    following_user = [follow.user for follow in following]

    posts = Post.objects.filter(author__in=following_user).order_by("-date_created")

    return render(request, "network/followers.html", {
        "posts": posts
    })