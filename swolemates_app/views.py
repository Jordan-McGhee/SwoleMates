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
    
    # empty list for user and friend objects to go into. This will be used to gather posts to show on the home page. I'm sure there's a much better way to do this, but my brain is fried and I have so much more to do. Please don't judge.

    user_and_friends = []

    # iterates over friends in a roundabout way. Can't iterate over a query object (learned that the hard way), so I iterate over the length of the friends query. Append user objects to my empty list. After the loop, I append the user as well. This will be used to check if a post.posted_by is equal to an object in this group 

    for i in range(len(friends)):
        user_and_friends.append(User.objects.get(username=friends[i].username))

    user_and_friends.append(User.objects.get(username=user.username))
    
    # grabs all friend request objects involving user

    # USER SENT
    user_sent_friend_requests = Friend_Request.objects.filter(sender = user)
    
    # USER RECEIVED
    user_received_friend_requests = Friend_Request.objects.filter(receiver = user)

    # empty lists to append usernames & objects to

    user_sent_request_usernames = []
    user_sent_request_objects = []
    
    user_received_request_usernames = []
    user_received_request_objects = []

    for i in range(len(user_sent_friend_requests)):
        user_sent_request_usernames.append(user_sent_friend_requests[i].receiver)
        user_sent_request_objects.append(User.objects.get(username=user_sent_friend_requests[i].receiver))

    print(f"{user.username} has sent requests to the following users: {user_sent_request_usernames}")

    for i in range(len(user_received_friend_requests)):
        user_received_request_usernames.append(user_received_friend_requests[i].sender)
        user_received_request_objects.append(user_received_friend_requests[i].sender)

    print(f"{user.username} has received requests from the following users: {user_received_request_usernames}. Objects: {user_received_request_objects}")

    context = {
        "user": user,
        "posts": all_posts,
        "friends": friends,
        "user_and_friends": user_and_friends,
        "all_others": all_other_users,
        "user_workouts": user.workouts.all(),
        "user_friend_requests": user_received_request_objects,
        "user_sent_requests": user_sent_request_objects
    }

    return render(request, "home.html", context)

def home_send_friend_request(request,username):
    if request.method == "POST":
        user = User.objects.get(id=request.session['user_id'])
        new_friend = User.objects.get(username = username)
        user_sent_friend_requests = Friend_Request.objects.filter(sender = user)

        Friend_Request.objects.create(sender=user, receiver=new_friend)

        print(f"{user.username} sent request to {new_friend.username}. User's sent requests: {user_sent_friend_requests}")

    return redirect(f'/swolemates')

def home_accept_friend_request(request,username):
    if request.method == "POST":
        user = User.objects.get(id=request.session['user_id'])
        new_friend = User.objects.get(username = username)
        friend_request = Friend_Request.objects.get(sender = new_friend, receiver = user)

        user.friends.add(new_friend)
        friend_request.delete()

    return redirect('/swolemates')

def home_deny_friend_request(request,username):
    if request.method == "POST":
        user = User.objects.get(id=request.session['user_id'])
        new_friend = User.objects.get(username = username)
        friend_request = Friend_Request.objects.get(sender = new_friend, receiver = user)

        friend_request.delete()

    return redirect('/swolemates')

def home_remove_friend(request,username):
    if request.method == "POST":
        user = User.objects.get(id=request.session['user_id'])
        removed_friend = User.objects.get(username = username)
        
        user.friends.remove(removed_friend)

    return redirect(f'/swolemates')

# HOME POST/COMMENT/LIKE CREATE/EDIT/DELETE
def home_post_create(request):
    user = User.objects.get(id=request.session['user_id'])
    if request.method == "POST":
        errors = Post.objects.validator(request.POST)

        if len(errors) > 0:
            if len(errors) > 0:
                for k, v in errors.items():
                    messages.error(request, v)
            return redirect('/swolemates')
        

        if request.POST['workout'] != "none":
            workout = Workout.objects.get(id=request.POST['workout'])

            post = Post.objects.create(
                content = request.POST['content'],
                image = request.FILES.get('image'),
                posted_by = User.objects.get(id=user.id),
                workout = workout
            )
            print(f"WORKOUT ADDED TO POST: {workout.name}")
            print(f"POST.WORKOUT = {post.workout}")

        else:
            Post.objects.create(
                content = request.POST['content'],
                image = request.FILES.get('image'),
                posted_by = User.objects.get(id = user.id)
            )
        
    return redirect('/swolemates')

def home_post_add_like(request,post_id):
    if request.method == "POST":

        user = User.objects.get(id=request.session['user_id'])
        post = Post.objects.get(id=post_id)

        user.liked_posts.add(post)
        # post.liked_by.add(user)
        print(user.liked_posts)

    return redirect(f'/swolemates')

def home_post_remove_like(request,post_id):
    if request.method == "POST":

        user = User.objects.get(id=request.session['user_id'])
        post = Post.objects.get(id=post_id)

        post.liked_by.remove(user)

    return redirect(f'/swolemates')


def home_post_add_comment(request,post_id):
    if request.method == "POST":
        errors = Comment.objects.validator(request.POST)

        if len(errors) > 0:
            for k, v in errors.items():
                messages.error(request, v)
            return redirect(f'/swolemates')

        user = User.objects.get(id=request.session['user_id'])
        post = Post.objects.get(id=post_id)

        new_comment = Comment.objects.create(content=request.POST['content'], post=post,posted_by=user)

    return redirect(f'/swolemates')

def home_post_delete_comment(request,post_id,comment_id):
    if request.method == "POST":

        post = Post.objects.get(id=post_id)
        comment = Comment.objects.get(id=comment_id)

        comment.delete()

    return redirect(f'/swolemates')

def home_comment_add_like(request,comment_id):
    if request.method == "POST":

        user = User.objects.get(id=request.session['user_id'])
        comment = Comment.objects.get(id=comment_id)

        user.liked_comments.add(comment)

    return redirect(f'/swolemates')

def home_comment_remove_like(request,comment_id):
    if request.method == "POST":

        user = User.objects.get(id=request.session['user_id'])
        comment = Comment.objects.get(id=comment_id)

        user.liked_comments.remove(comment)

    return redirect(f'/swolemates')



# PROFILE PAGE

def profile(request, username):
    user = User.objects.get(id=request.session['user_id'])
    profile = User.objects.get(username=username)

    # grabs all friend request objects involving user

    # USER SENT
    user_sent_friend_requests = Friend_Request.objects.filter(sender = user)
    
    # USER RECEIVED
    user_received_friend_requests = Friend_Request.objects.filter(receiver = user)

    # empty lists to append usernames & objects to

    user_sent_request_usernames = []
    user_sent_request_objects = []
    
    user_received_request_usernames = []
    user_received_request_objects = []

    for i in range(len(user_sent_friend_requests)):
        user_sent_request_usernames.append(user_sent_friend_requests[i].receiver)
        user_sent_request_objects.append(User.objects.get(username=user_sent_friend_requests[i].receiver))

    print(f"{user.username} has sent requests to the following users: {user_sent_request_usernames}")

    for i in range(len(user_received_friend_requests)):
        user_received_request_usernames.append(user_received_friend_requests[i].sender)
        user_received_request_objects.append(user_received_friend_requests[i].sender)

    print(f"{user.username} has received requests from the following users: {user_received_request_usernames}. Objects: {user_received_request_objects}")


    context = {
        "user": user,
        "profile": profile,
        "posts": profile.posts.all(),
        "user_friends": user.friends.all(),
        "profile_friends": profile.friends.all(),
        "all_others": User.objects.exclude(id=user.id),
        "profile_workouts": profile.workouts.all(),
        "user_friend_requests": user_received_request_objects,
        # "user_friend_requests_usernames": user_received_request_usernames,
        "user_sent_requests": user_sent_request_objects
    }


    return render(request, "profile.html", context)

# PROFILE EDIT/UPDATE

def profile_edit(request,username):
    context = {
        "user": User.objects.get(id=request.session['user_id'])
    }

    return render(request,"edit_profile.html", context)

def profile_update(request,username):
    if request.method == "POST":
        user = User.objects.get(id=request.session['user_id'])

        user.profile_photo = request.FILES.get("profile_photo") or user.profile_photo
        user.bio = request.POST['bio']
        user.fav_exercises = request.POST['fav_exercises']
        user.save()
        
    return redirect(f'/swolemates/user/{user.username}')

# PROFILE POST/COMMENT/LIKE CREATE/EDIT/DELETE

def profile_post_create(request, username):
    if request.method == "POST":
        errors = Post.objects.validator(request.POST)

        if len(errors) > 0:
            for k, v in errors.items():
                messages.error(request, v)
            return redirect(f'/swolemates/user/{username}')
        
        if request.POST['workout'] != "none":
            workout = Workout.objects.get(id=request.POST['workout'])

            post = Post.objects.create(
                content = request.POST['content'],
                image = request.FILES.get('image'),
                posted_by = User.objects.get(username=username),
                workout = workout
            )
            print(f"WORKOUT ADDED TO POST: {workout.name}")
            print(f"POST.WORKOUT = {post.workout}")

        else:
            Post.objects.create(
                content = request.POST['content'],
                image = request.FILES.get('image'),
                posted_by = User.objects.get(username=username)
            )
        
    return redirect(f'/swolemates/user/{username}')


def profile_post_add_like(request,username,post_id):
    if request.method == "POST":

        user = User.objects.get(id=request.session['user_id'])
        profile = User.objects.get(username=username)
        post = Post.objects.get(id=post_id)

        user.liked_posts.add(post)
        # post.liked_by.add(user)
        print(user.liked_posts)

    return redirect(f'/swolemates/user/{username}')

def profile_post_remove_like(request,username,post_id):
    if request.method == "POST":

        user = User.objects.get(id=request.session['user_id'])
        profile = User.objects.get(username=username)
        post = Post.objects.get(id=post_id)

        post.liked_by.remove(user)

    return redirect(f'/swolemates/user/{username}')


def profile_add_comment(request,username,post_id):
    if request.method == "POST":
        errors = Comment.objects.validator(request.POST)

        if len(errors) > 0:
            for k, v in errors.items():
                messages.error(request, v)
            return redirect(f'/swolemates/user/{username}')

        user = User.objects.get(id=request.session['user_id'])
        profile = User.objects.get(username=username)
        post = Post.objects.get(id=post_id)

        new_comment = Comment.objects.create(content=request.POST['content'], post=post,posted_by=user)

    return redirect(f'/swolemates/user/{username}')

def profile_delete_comment(request,username,post_id,comment_id):
    if request.method == "POST":

        user = User.objects.get(id=request.session['user_id'])
        profile = User.objects.get(username=username)
        post = Post.objects.get(id=post_id)
        comment = Comment.objects.get(id=comment_id)

        comment.delete()

    return redirect(f'/swolemates/user/{username}')

def profile_comment_add_like(request,username,comment_id):
    if request.method == "POST":

        user = User.objects.get(id=request.session['user_id'])
        comment = Comment.objects.get(id=comment_id)

        user.liked_comments.add(comment)

    return redirect(f'/swolemates/user/{username}')

def profile_comment_remove_like(request,username,comment_id):
    if request.method == "POST":

        user = User.objects.get(id=request.session['user_id'])
        comment = Comment.objects.get(id=comment_id)

        user.liked_comments.remove(comment)

    return redirect(f'/swolemates/user/{username}')


# PROFILE SEND/ACCEPT/DENY/REMOVE FRIEND REQUESTS

def profile_send_friend_request(request, username):
    if request.method == "POST":
        user = User.objects.get(id=request.session['user_id'])
        new_friend = User.objects.get(username = username)
        user_sent_friend_requests = Friend_Request.objects.filter(sender = user)

        Friend_Request.objects.create(sender=user, receiver=new_friend)

        print(f"{user.username} sent request to {new_friend.username}. User's sent requests: {user_sent_friend_requests}")

    return redirect(f'/swolemates/user/{user.username}')

def profile_accept_friend_request(request,username):
    if request.method == "POST":
        user = User.objects.get(id=request.session['user_id'])
        new_friend = User.objects.get(username = username)
        friend_request = Friend_Request.objects.get(sender = new_friend, receiver = user)

        user.friends.add(new_friend)
        friend_request.delete()

    return redirect(f'/swolemates/user/{user.username}')

def profile_deny_friend_request(request,username):
    if request.method == "POST":
        user = User.objects.get(id=request.session['user_id'])
        new_friend = User.objects.get(username = username)
        friend_request = Friend_Request.objects.get(sender = new_friend, receiver = user)

        friend_request.delete()

    return redirect(f'/swolemates/user/{user.username}')

def profile_remove_friend(request,username):
    if request.method == "POST":
        user = User.objects.get(id=request.session['user_id'])
        removed_friend = User.objects.get(username = username)
        
        user.friends.remove(removed_friend)

    return redirect(f'/swolemates/user/{user.username}')


# POST VIEW/EDIT/UPDATE/DELETE ADD/REMOVE COMMENTS/LIKES

def view_post(request,post_id):
    post = Post.objects.get(id=post_id)

    context = {
        "user": User.objects.get(id=request.session["user_id"]),
        "profile": post.posted_by,
        "post": post,
    }

    return render(request, "post_view.html", context)

def edit_post(request,post_id):
    context = {
        "post": Post.objects.get(id=post_id),
        "user": User.objects.get(id=request.session["user_id"])
    }

    return render(request,"post_edit.html", context)

def update_post(request,post_id):
    if request.method == "POST":
        errors = Post.objects.validator(request.POST)
        print(errors)
        if len(errors) > 0:
            for k, v in errors.items():
                messages.error(request, v)

            print("there were errors")
            return redirect(f'/swolemates/post/{post_id}/edit')
        
        if request.POST['workout'] != "none":
            workout = Workout.objects.get(id=request.POST['workout'])
            
            post = Post.objects.get(id=post_id)
            post.content = request.POST['content']
            post.workout = workout
            post.image = request.FILES.get('image') or post.image
            post.save()

        else:

            post = Post.objects.get(id=post_id)
            post.content = request.POST['content']
            post.image = request.FILES.get('image') or post.image
            post.save()

    return redirect(f"/swolemates/post/{post_id}")

def delete_post(request,post_id):
    if request.method == "POST":
        post = Post.objects.get(id=post_id)
        user = User.objects.get(id=request.session["user_id"])
        post.delete()

        return redirect(f"/swolemates/user/{user.username}")
    
    return redirect(f"/swolemates/post/{post_id}")

def post_add_like(request,post_id):
    if request.method == "POST":

        user = User.objects.get(id=request.session['user_id'])
        post = Post.objects.get(id=post_id)

        user.liked_posts.add(post)
        # post.liked_by.add(user)
        print(user.liked_posts)

    return redirect(f'/swolemates/post/{post_id}')

def post_remove_like(request,post_id):
    if request.method == "POST":

        user = User.objects.get(id=request.session['user_id'])
        post = Post.objects.get(id=post_id)

        post.liked_by.remove(user)

    return redirect(f'/swolemates/post/{post_id}')


def post_add_comment(request,post_id):
    if request.method == "POST":
        errors = Comment.objects.validator(request.POST)

        if len(errors) > 0:
            for k, v in errors.items():
                messages.error(request, v)
            return redirect(f'/swolemates/post/{post_id}')

        user = User.objects.get(id=request.session['user_id'])
        post = Post.objects.get(id=post_id)

        new_comment = Comment.objects.create(content=request.POST['content'], post=post,posted_by=user)

    return redirect(f'/swolemates/post/{post_id}')

def post_delete_comment(request,post_id,comment_id):
    if request.method == "POST":

        comment = Comment.objects.get(id=comment_id)

        comment.delete()

    return redirect(f'/swolemates/post/{post_id}')

def post_comment_add_like(request,post_id,comment_id):
    if request.method == "POST":

        user = User.objects.get(id=request.session['user_id'])
        comment = Comment.objects.get(id=comment_id)

        user.liked_comments.add(comment)

    return redirect(f'/swolemates/post/{post_id}')

def post_comment_remove_like(request,post_id,comment_id):
    if request.method == "POST":

        user = User.objects.get(id=request.session['user_id'])
        comment = Comment.objects.get(id=comment_id)

        user.liked_comments.remove(comment)

    return redirect(f'/swolemates/post/{post_id}')

# FRIENDS LIST

def friends_list(request, username):
    user = User.objects.get(id=request.session['user_id'])
    profile = User.objects.get(username=username)
    
    # grabs all friend request objects involving user

    # USER SENT
    user_sent_friend_requests = Friend_Request.objects.filter(sender = user)
    
    # USER RECEIVED
    user_received_friend_requests = Friend_Request.objects.filter(receiver = user)

    # empty lists to append usernames & objects to

    user_sent_request_usernames = []
    user_sent_request_objects = []
    
    user_received_request_usernames = []
    user_received_request_objects = []

    for i in range(len(user_sent_friend_requests)):
        user_sent_request_usernames.append(user_sent_friend_requests[i].receiver)
        user_sent_request_objects.append(User.objects.get(username=user_sent_friend_requests[i].receiver))

    print(f"{user.username} has sent requests to the following users: {user_sent_request_usernames}")

    for i in range(len(user_received_friend_requests)):
        user_received_request_usernames.append(user_received_friend_requests[i].sender)
        user_received_request_objects.append(user_received_friend_requests[i].sender)

    print(f"{user.username} has received requests from the following users: {user_received_request_usernames}. Objects: {user_received_request_objects}")

    context = {
        "user": user,
        "profile": profile,
        "profile_friends": profile.friends.all(),
        "all_others": User.objects.exclude(id=user.id),
        "user_friend_requests": user_received_request_objects,
        # "user_friend_requests_usernames": user_received_request_usernames,
        "user_sent_requests": user_sent_request_objects
    }

    return render(request, "friends_list.html", context)

def friends_send_friend_request(request,username):
    if request.method == "POST":
        user = User.objects.get(id=request.session['user_id'])
        new_friend = User.objects.get(username = username)
        user_sent_friend_requests = Friend_Request.objects.filter(sender = user)

        Friend_Request.objects.create(sender=user, receiver=new_friend)

        print(f"{user.username} sent request to {new_friend.username}. User's sent requests: {user_sent_friend_requests}")

    return redirect(f'/swolemates/user/{user.username}/friends')

def friends_accept_friend_request(request,username):
    if request.method == "POST":
        user = User.objects.get(id=request.session['user_id'])
        new_friend = User.objects.get(username = username)
        friend_request = Friend_Request.objects.get(sender = new_friend, receiver = user)

        user.friends.add(new_friend)
        friend_request.delete()

    return redirect(f'/swolemates/user/{user.username}/friends')

def friends_deny_friend_request(request,username):
    if request.method == "POST":
        user = User.objects.get(id=request.session['user_id'])
        new_friend = User.objects.get(username = username)
        friend_request = Friend_Request.objects.get(sender = new_friend, receiver = user)

        friend_request.delete()

    return redirect(f'/swolemates/user/{user.username}/friends')

def friends_remove_friend(request,username):
    if request.method == "POST":
        user = User.objects.get(id=request.session['user_id'])
        removed_friend = User.objects.get(username = username)
        
        user.friends.remove(removed_friend)

    return redirect(f'/swolemates/user/{user.username}/friends')

# WORKOUT LIST

def workouts_list(request, username):
    user = User.objects.get(id=request.session['user_id'])
    profile = User.objects.get(username=username)

    context = {
        "user": user,
        "profile": profile,
        "workouts": profile.workouts.all()
    }

    return render(request, "workouts_list.html", context)

# WORKOUT PAGES

def workout_form(request):
    return render(request, "workout_create.html")

def workout_create(request):
    if request.method == "POST":
        user = User.objects.get(id=request.session['user_id'])
        errors = Workout.objects.validator(request.POST)
        
        if len(errors) > 0:
            for k, v in errors.items():
                messages.error(request, v)
            return redirect(f'/swolemates/workout')

        workout = Workout.objects.create(name=request.POST['workout_name'], created_by=user)

        for i in range(1,9):
            if request.POST[f'name{i}'] != "":
                print(request.POST[f'name{i}'])
                Exercise.objects.create(workout=workout, name=request.POST[f'name{i}'],set_count=request.POST[f'sets{i}'], rep_count=request.POST[f'reps{i}'])

        return redirect(f'/swolemates/workout/{workout.id}')

    return redirect('/swolemates/workout')

def workout_view(request, id):
    workout = Workout.objects.get(id=id)

    context = {
        "workout": workout,
        "user": User.objects.get(id=request.session['user_id']),
        "exercises": workout.exercises.all()
    }

    return render(request, "workout_view.html", context)

def workout_edit(request, id):
    workout = Workout.objects.get(id=id)

    context = {
        "workout": workout,
        "user": User.objects.get(id=request.session['user_id']),
        "exercises": workout.exercises.all()
    }

    return render(request, "workout_edit.html", context)

def workout_update(request, id):
    workout = Workout.objects.get(id=id)

    workout.name = request.POST['workout_name']

    for i,exercise in enumerate(workout.exercises.all()):
        
        exercise.name = request.POST[f'name{i+1}']
        exercise.set_count = request.POST[f'sets{i+1}']
        exercise.rep_count = request.POST[f'reps{i+1}']

        exercise.save()
        

    workout.save()

    return redirect(f"/swolemates/workout/{id}")

def workout_delete(request, id):
    if request.method == "POST":
        user = User.objects.get(id=request.session['user_id'])

        workout = Workout.objects.get(id=id)
        workout.delete()

        return redirect(f"/swolemates/user/{user.username}/workouts")
