from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post, Like, Comment, Follow

import json
from math import ceil


def index(request):
    return render(request, "network/index.html")


@login_required
def follow(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=400)
    
    body = json.loads(request.body)
    username = body["username"]

    follower = request.user
    followed = User.objects.get(username=username)
    if follower == followed:
        return JsonResponse({"error": "Can't follow yourself"}, status=400)
    
    try:
        follow = Follow(follower=follower, followed=followed)
        follow.save()
        return JsonResponse({"message": "followed user successfully"}, status=201)
    except IntegrityError:
        return JsonResponse({"error": "Can't follow the same user twice"}, status=400)
        

@login_required
def unfollow(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=400)
    
    body = json.loads(request.body)
    username = body["username"]

    try:
        followed = User.objects.get(username=username)
        follow = Follow.objects.get(follower=request.user, followed=followed)
        follow.delete()
    except Follow.DoesNotExist:
        return JsonResponse({"error": "You're not following this user to unfollow"}, status=400)
    
    return JsonResponse({"message": "Unfollowed user successfully"}, status=201)
    

@login_required
def following(request):
    return render(request, "network/following.html")


@login_required
def following_posts(request, page):
    start = page * 10 - 10
    user = User.objects.get(username=request.user.username)
    following = User.objects.filter(followers__follower=user)
    posts = Post.objects.order_by('-timestamp').filter(user__in=following)[start : 10 + start]

    return JsonResponse([post.serialize(request.user) for post in posts], safe=False)


@login_required
def max_page_following(request):
    user = User.objects.get(username=request.user.username)
    following = User.objects.filter(followers__follower=user)
    page_max = ceil(Post.objects.filter(user__in=following).count() / 10)

    return JsonResponse({
        'page_max': f"{page_max}"
    }, status=201)


@login_required
def like(request, post_id):
    if request.method != "POST":
        return JsonResponse({"message": "POST method required"}, status=400)
    
    post = Post.objects.get(pk=post_id)
    is_like = json.loads(request.body)["like"]
    
    # Like post
    if is_like:
        like = Like(user=request.user, post=post)
        try:
            like.save()
            return JsonResponse({"message": f"Liked post: {post_id}"}, status=201)
        except IntegrityError:
            return JsonResponse({
                "error": f"Post {post_id} already liked by {request.user.username}"
                }, status=400)
        
    # Unlike post
    try:
        like = Like.objects.get(user=request.user, post=post)
        like.delete()
        return JsonResponse({"message": f"Unliked {post_id} successfully"}, status=201)
    except Like.DoesNotExist:
        return JsonResponse({"error": "Unlike failed because like doesn't exist"}, status=400)


def user(request, username):
    try:
        user_v = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse(f"Error, an account with the username {username} does not exist")
    
    follower_count = user_v.followers.count()
    followed_count = user_v.following.count()
    already_following = Follow.objects.filter(follower=request.user, followed=user_v).exists()

    return render(request, "network/user.html", {
        'user_v': user_v,
        'follower_count': follower_count,
        'followed_count': followed_count,
        'already_following': already_following
    })


def user_posts(request, username, page):
    user = User.objects.get(username=username)
    start = page * 10 - 10
    posts = Post.objects.order_by('-timestamp').filter(user=user)[start : 10 + start]

    if request.user.is_authenticated:
        return JsonResponse([post.serialize(request.user) for post in posts], safe=False)
    return JsonResponse([post.serialize() for post in posts], safe=False)


# returns json for infinite scrolling
def all_posts(request, page):
    start = page * 10 - 10
    posts = Post.objects.order_by('-timestamp').all()[start : 10 + start]

    if request.user.is_authenticated:
        return JsonResponse([post.serialize(request.user) for post in posts], safe=False)
    return JsonResponse([post.serialize() for post in posts], safe=False)


def max_page(request, username):
    if username != "index":
        page_max = ceil(Post.objects.filter(user=User.objects.get(username=username)).count() / 10)
    else:
        page_max = ceil(Post.objects.count() / 10)

    return JsonResponse({
        'page_max': f"{page_max}"
    }, status=201)


def comments(request, post_id, page):
    start = page * 10 - 10
    post = Post.objects.get(pk=post_id)
    comments = Comment.objects.order_by("-timestamp").filter(post=post)[start : start + 10]

    return JsonResponse([comment.serialize() for comment in comments], safe=False)


def new_comment(request, post_id):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)
    text = data['text'].strip()
    if not text or text == '':
        return JsonResponse({"error": "Comment cannot be empty."}, status=400)

    comment = Comment(user=request.user, text=text, post=Post.objects.get(pk=post_id))
    comment.save()
    
    return JsonResponse({
        "message": "Post created successfully.",
        "comment": comment.serialize()
        }, status=201)


def max_page_comments(request, post_id):
    page_max = ceil(Comment.objects.filter(post=Post.objects.get(pk=post_id)).count() / 10)

    return JsonResponse({
        'page_max': f"{page_max}"
    }, status=201)


def post_view(request, post_id):
    return render(request, "network/post_view.html", {
        "post_id": post_id
    })


def post(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "This post does not exist"}, status=404)

    if request.user.is_authenticated:
        return JsonResponse(post.serialize(request.user), safe=False)
    return JsonResponse(post.serialize(), safe=False)


@login_required
def post_edit(request, post_id):
    if request.method != "PUT":
        return JsonResponse({"error": "PUT method required"}, status=400)

    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": f"Post with id {post_id} does not exist"}, status=404)
    
    new_text = json.loads(request.body)["text"].strip()

    if not new_text or new_text == '':
        return JsonResponse({"error": "Post cannot be empty."}, status=400)
    
    if request.user != post.user:
        return JsonResponse({"error": "You can't edit a post that isn't your own"}, status=400)
    
    post.text = new_text
    post.save()
    return JsonResponse({"message": "Edit successful"}, status=200)
    


@login_required
def new_post(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)
    text = data['text'].strip()
    if not text or text == '':
        return JsonResponse({"error": "Post cannot be empty."}, status=400)

    post = Post(user=request.user, text=text)
    post.save()
    
    return JsonResponse({
        "message": "Post created successfully.",
        "post": post.serialize()
        }, status=201)


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
