import json
from django.core import serializers
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *


def index(request):
    return render(request, "network/index.html")


@login_required
def following(request):
    return render(request, "network/following.html")


def follow(request, userID):
    followedUser = User.objects.get(username=userID)
    followerUser = User.objects.get(username=request.user)

    if not FollowUser.objects.filter(
            follower=followerUser, followed=followedUser).exists():
        follow = FollowUser.objects.create(
            follower=followerUser, followed=followedUser, follow=True)
        follow.save()
        print("save done")
        followerCount = FollowUser.objects.filter(
            followed=followedUser)
        return JsonResponse(serializers.serialize('json', [followerCount]), safe=False)

    follow = FollowUser.objects.get(
        follower=followerUser, followed=followedUser)
    print(follow.follow)
    if follow.follow == True:
        follow.follow = False
    else:
        print(follow.follow)
        follow.follow = True
    follow.save()
    followersCount = FollowUser.objects.filter(
        followed=followedUser, follow=True)
    print(followersCount)
    return JsonResponse([followerCount.serialize() for followerCount in followersCount], safe=False)


def userPage(request, username):
    user = User.objects.get(username=username)
    posts = Post.objects.filter(user=user)
    followed = FollowUser.objects.filter(followed=user, follow=True).count()
    follower = FollowUser.objects.filter(follower=user).count()
    if not request.user.is_authenticated:
        return render(request, "network/user.html", {
            "user": user,
            "posts": posts,
            "followed": followed,
            "follower": follower
        })
    owner = User.objects.get(username=request.user)
    try:
        follow = FollowUser.objects.get(follower=owner, followed=user)
    except:
        follow = FollowUser.DoesNotExist
    print(user)
    return render(request, "network/user.html", {
        "user": user,
        "posts": posts,
        "followed": followed,
        "follower": follower,
        "follow": follow
    })


def show_posts(request, postbox):
    # If post method
    if request.method == "POST":
        submit_post(request)

    # If get method
    # Check "postbox"
    if postbox == "show_posts":
        posts = Post.objects.filter(
            archived=False
        )
    if postbox == "following":
        # user = User.objects.get(username=request.user)
        # following = user.UserFollowed.get(follower=user)
        posts = Post.objects.filter(
            archived=False,
            # user=following
        )
    else:
        JsonResponse({"error": "Invalid postbox"}, status=400)
    posts = posts.order_by("-timestamp").all()
    return JsonResponse([post.serialize() for post in posts], safe=False)


@login_required
def submit_post(request):
    print("request is post")
    data = json.loads(request.body)
    body = data.get("body", "")
    print(body)
    user = data.get("user", "")
    print(user)
    username = User.objects.get(username=user)
    if not body:
        return JsonResponse({
            "error": "Body of post is empty."
        })
    post = Post(
        user=username,
        body=body
    )
    post.save()
    return JsonResponse({"message": "Post sent successfully."}, status=201)


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
