from django.contrib.auth import authenticate, login, logout
from django.core import paginator
from django.db import IntegrityError
from django.db.models.deletion import PROTECT
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse
import json
from .models import Follow, User, Post, Like
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    if request.method == "POST" and request.POST.get('content') != None:
        content = str(request.POST.get('content'))
        if len(content.strip()) <= 0:
            return HttpResponseRedirect(reverse('index'))
        try:
            Like.objects.create(like=0, post_id=int(Post.objects.last().id+1))
        except AttributeError:
            Like.objects.create(like=0, post_id=1)
        Post.objects.create(user=request.user, content=content, like=Like.objects.last())
    # edit feature
    if request.method == "POST" and request.POST.get('content') == None:
        data = json.loads(request.body)
        new_content = str(data.get('newcontent', '')).replace(':D', '😁').replace(":)", '🙂')
        post_id = data.get('post', '')
        post = Post.objects.get(id=post_id)
        post.content = new_content
        post.save()

    posts = Post.objects.order_by('-time')
    post_paginator = Paginator(posts, 10)
    page_num = request.GET.get('page')
    page = post_paginator.get_page(page_num)
    return render(request, "network/index.html", {
        "count": posts.count,
        "page": page,
        "n": range(1, post_paginator.num_pages + 1)
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST.get("username")
        password = request.POST.get("password")
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
        username = request.POST.get("username")
        email = request.POST.get("email")

        # Ensure password matches confirmation
        password = request.POST.get("password")
        confirmation = request.POST.get("confirmation")
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
def profile(request, username):
    context = {}
    try:
        user = User.objects.get(username=username)
        try:
            follow = Follow.objects.get(user=user).following.count()
        except:
            follow = 0
        context = {
            "posts":Post.objects.filter(user=user).order_by('-time'),
            "profile": user,
            "following": follow,
            "followers": Follow.objects.filter(following=user).count(),
            "follow": Follow.objects.filter(user=request.user, following=user).exists()
        }
    except:
        context = {
            "error": "User not found!"        
        }
    return render(request, 'network/profile.html', context)
@login_required
def like(request, id):
    if request.method != "POST":
        return JsonResponse({"error":"No post method found!", "post": id})
    data = json.loads(request.body)
    likes = data.get('like', '')
    unlike = data.get('unlike', '')
    try:
        like = Like.objects.get(post_id=id)
        like.like = likes
        like.save()
        post = Post.objects.get(id=id)
        if unlike:
            post.liked.remove(request.user)
        else:
            post.liked.add(request.user)
        post.like = like
        post.save()
    except:
        return JsonResponse({"error":"Post method not found!"})
    return JsonResponse({"result":"success"})
@login_required
def follow(request):
    if request.method == "GET":
        try:
            follow = Follow.objects.get(user=request.user).following.all()
            posts = []
            for user in follow:
                posts.append(Post.objects.filter(user=user))
            return render(request, "network/following.html", {
                "posts":posts       
            })
        except:
            return render(request, "network/following.html", {
                "message":"You haven't follow anyone :)"
            })
    data = json.loads(request.body)
    follow_user = data.get('user', '')
    unfollow = data.get('unfollow', '')
    user = User.objects.get(username=request.user)
    follow_user = User.objects.get(username=follow_user)
    if unfollow:
        Follow.objects.get(user=user, following=follow_user).delete()
    else:
        if Follow.objects.filter(user=user).count() > 0:
            Follow.objects.get(user=user).following.add(follow_user)
        else:
            follow = Follow()
            follow.user = user
            follow.save()
            follow.following.add(follow_user)
    return JsonResponse({"message":"successfully follow/unfollow this user"})