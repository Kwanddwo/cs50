from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post, Like, Comment

import json

def index(request):
    return render(request, "network/index.html")


# returns json for infinite scrolling, 15 posts per scroll. Implement this later on!!!
def all_posts(request, start):
    posts = []

    for i in range(start, start + 15):
        try:
            posts.append(Post.objects.get(pk=i))
        except Post.DoesNotExist:
            break

    return JsonResponse([post.serialize() for post in posts]) # Might need safe=False

def comments(request, post_id):
    post = Post.objects.get(pk=post_id)
    comments = Comment.objects.filter(post=post)

    # Reverse chronological order
    comments = comments.order_by("-timestamp").all()
    return JsonResponse([comment.serialize() for comment in comments]) # Might also need safe=False


@login_required
def new_post(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)
    if not data.text:
        return JsonResponse({"error": "Post cannot be empty."}, status=400)

    post = Post(user=request.user, text=data.text)
    post.save()
    
    return JsonResponse({"message": "Post created successfully."}, status=201)


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
