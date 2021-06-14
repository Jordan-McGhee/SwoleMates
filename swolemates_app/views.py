from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages

# LOGIN/REGISTER

def index(request):
    return render(request, "login_reg.html")

def register(request):
    if request.method == "POST":
        errors = User.objects.validator(request.POST)

        if len(errors) > 0:
            for k, v in errors.items():
                messages.error(request, v)
            return redirect('/')

        new_user = User.objects.register(request.POST)
        request.session['user_id'] = new_user.id

        return redirect('/swolemates')

    return redirect('/')

def login(request):
    if request.method=="POST":
        
        if not User.objects.authenticate(request.POST['email'], request.POST['password']):
            messages.error(request, "Invalid Email/Password")
            return redirect('/')

        user = User.objects.get(email = request.POST['email'])
        request.session['user_id'] = user.id

        return redirect('/swolemates')

    return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')

# MAIN PAGE

def home(request):
    if 'user_id' not in request.session:
        return redirect('/')

    user = User.objects.get(id=request.session['user_id'])
    all_posts = Post.objects.all()
    friends = user.friends.all()
    all_other_users = User.objects.exclude(id=user.id)

    context = {
        "user": user,
        "posts": all_posts,
        "friends": friends,
        "all_others": all_other_users,
        "user_workouts": user.workouts.all()
        # "friends_workouts": friends.workouts
    }

    return render(request, "home.html", context)

def home_post_create(request):
    user = User.objects.get(id=request.session['user_id'])
    if request.method == "POST":
        errors = Post.objects.validator(request.POST)

        if len(errors) > 0:
            if len(errors) > 0:
                for k, v in errors.items():
                    messages.error(request, v)
            return redirect('/swolemates')
        
        Post.objects.create(
            content = request.POST['content'],
            image = request.FILES.get('image'),
            posted_by = User.objects.get(id = user.id)
        )
        
    return redirect('/swolemates')

# PROFILE PAGE

def profile(request, username):
    user = User.objects.get(id=request.session['user_id'])
    profile = User.objects.get(username=username)
    print(profile.first_name)

    context = {
        "user": user,
        "profile": profile,
        "posts": profile.posts.all(),
        "profile_friends": profile.friends.all(),
        "all_others": User.objects.exclude(id=user.id),
        "profile_workouts": profile.workouts.all()
    }

    return render(request, "profile.html", context)

def profile_post_create(request, username):
    if request.method == "POST":
        errors = Post.objects.validator(request.POST)

        if len(errors) > 0:
            if len(errors) > 0:
                for k, v in errors.items():
                    messages.error(request, v)
            return redirect(f'/swolemates/{username}')
        
        Post.objects.create(
            content = request.POST['content'],
            image = request.FILES.get('image'),
            posted_by = User.objects.get(username=username)
        )
        
    return redirect(f'/swolemates/{username}')

