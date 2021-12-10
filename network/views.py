import json
from django.core import serializers
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

from .models import *


def index(request):
    posts = Post.objects.filter(
        archived=False
    )
    posts = posts.order_by("-timestamp").all()
    if LikePost.objects.filter(post__in=posts, like=True).exists():
        liked = LikePost.objects.filter(
            post__in=posts, like=True)

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {'posts': page_obj, 'liked': liked})


@login_required
def following(request):
    user = User.objects.get(username=request.user.username)
    following = FollowUser.objects.filter(
        follower=user, follow=True).values_list('followed', flat=True)
    posts = Post.objects.filter(
        archived=False,
        user__in=following
    )
    posts = posts.order_by("-timestamp").all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/following.html", {"posts": page_obj})


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
    return JsonResponse({'status': 201, "follower_count": followersCount.count()}, status=201)


def userPage(request, username):
    user = User.objects.get(username=username)
    posts = Post.objects.filter(user=user)
    followed = FollowUser.objects.filter(followed=user, follow=True).count()
    follower = FollowUser.objects.filter(follower=user).count()
    posts = posts.order_by("-timestamp").all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if not request.user.is_authenticated:
        return render(request, "network/user.html", {
            "user": user,
            "posts": page_obj,
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
        "posts": page_obj,
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
        user = User.objects.get(username=request.user.username)
        following = FollowUser.objects.filter(
            follower=user, follow=True).values_list('followed', flat=True)
        print(following)
        print(following)
        print("ok")
        posts = Post.objects.filter(
            archived=False,
            user__in=following
        )
        print(posts)
    else:
        return HttpResponse(request, {"error": "Invalid postbox"}, status=400)

    posts = posts.order_by("-timestamp").all()
    paginator = Paginator(posts, 10)
    if request.GET.get("page") != None:
        try:
            posts = paginator.page(request.GET.get("page"))
        except:
            posts = paginator.page(1)
    else:
        posts = paginator.page(1)
    return render(request, 'network/{{postbox}}.html', {'posts': posts})


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


@login_required
def like(request, postID):
    likededPost = Post.objects.get(id=postID)
    LikeUser = User.objects.get(username=request.user)

    if not LikePost.objects.filter(
            user=LikeUser, post=likededPost).exists():
        like = LikePost.objects.create(
            user=LikeUser, post=likededPost, like=True)
        like.save()
        print("save done")
        likeCount = LikePost.objects.filter(
            post=likededPost, like=True)
        return JsonResponse({'status': 201, "like_count": likeCount.count()}, status=201)

    like = LikePost.objects.get(
        user=LikeUser, post=likededPost)
    if like.like == True:
        like.like = False
    else:
        like.like = True
    like.save()
    liked = like.like
    likeCount = LikePost.objects.filter(
        post=likededPost, like=True)
    return JsonResponse({'status': 201, "like_count": likeCount.count(), "liked": liked}, status=201)


def like_count(request, postID):
    likededPost = Post.objects.get(id=postID)
    LikeUser = User.objects.get(username=request.user)

    liked = LikePost.objects.filter(
        user=LikeUser, post=likededPost, like=True).exists()
    likeCount = LikePost.objects.filter(
        post=likededPost, like=True).count()
    return JsonResponse({'status': 201, "like_count": likeCount, "liked": liked}, status=201)


def like_count_notloggin(request, postID):
    likededPost = Post.objects.get(id=postID)
    likeCount = LikePost.objects.filter(
        post=likededPost, like=True).count()
    return JsonResponse({'status': 201, "like_count": likeCount}, status=201)


@login_required
def editPost(request, postID):
    user = User.objects.get(username=request.user)
    post = Post.objects.get(id=postID)
    body = post.body
    if not user == post.user:
        return JsonResponse({'error': 'User is not user'})
    return JsonResponse({'status': 201, "post": body}, status=201)


@csrf_exempt
@login_required
def editPostInDB(request):
    user = User.objects.get(username=request.user)
    data = json.loads(request.body)
    body = data.get("body", "")
    postID = data.get("postid", "")
    if not body:
        return JsonResponse({"error": "Body of post is empty."}, status=400)
    post = Post.objects.get(id=postID)
    if user != post.user:
        return JsonResponse({"error": "User request is not owner."}, status=400)
    post.body = body
    post.save()
    return JsonResponse({'status': 201, "post": post}, status=201)
