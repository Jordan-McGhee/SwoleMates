from django.db import models
from django.db.models.fields import related
import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
forbidden_chars = ['@#$%^&*()_+=[{/}\|]?,;:.~`!"']
banned_usernames = ["swolemate","swolemates","user","users","home","friend","friends","post","posts","request","requests","workout","workouts"]
banned_words = ["fuck","shit","ass","pussy","cunt","dick","balls","nigger","nigga","fag","faggot"]

# MODEL MANAGERS

class UserManager(models.Manager):
    def validator(self, postData):

        errors = {}

        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 letters long"

        if not postData['first_name'].isalpha():
            errors['first_name_alpha'] = "First name must contain letters only"

        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 letters long"

        if not postData['last_name'].isalpha():
            errors['last_name_alpha'] = "Last name must contain letters only"

        if len(postData['username']) < 5:
            errors['username'] = "Username must be at least 6 letters long"
        
        for char in forbidden_chars:
            if char in postData['username']:
                errors['username'] = "You used an invalid character. Username can only contain letters and numbers."

        username_unique_check = User.objects.filter(username=postData['username'])

        if username_unique_check:
            errors['username'] = "That username is already taken"

        if postData['username'] in banned_usernames:
            errors['username'] = "Please choose a different username"

        for word in banned_words:
            if word in postData['username'].lower():
                errors['username'] = "Really? Don't use those words in your username. Jerk."

        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Please enter a valid email address."

        email_unique_check = User.objects.filter(email=postData['email'])

        if email_unique_check:
            errors['email'] = "Please enter a unique email."


        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters."

        if postData['password'] != postData['confirm_password']:
            errors['confirm'] = "Passwords did not match"

        return errors

    def register(self, postData):
        safe_password = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt()).decode()

        return User.objects.create(first_name=postData['first_name'], last_name=postData['last_name'], username=postData['username'], email=postData['email'], password = safe_password)

    def authenticate(self, email, password):
        users = User.objects.filter(email = email)
        if users:
            user = users[0]
            if bcrypt.checkpw(password.encode(), user.password.encode()):
                return True
        
        return False

class PostCommentManager(models.Manager):
    def validator(self, postData):
        errors = {}

        if len(postData['content']) < 1:
            errors['content'] = "Post/Comment can't be empty"

        return errors

class WorkoutManager(models.Manager):
    def validator(self, postData):
        errors = {}

        if len(postData['workout_name']) < 1:
            errors["workout_name"] = "Workout name can't be empty"

        return errors

#  MODELS
class User(models.Model):
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    username = models.CharField(max_length=45, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length = 60)
    profile_photo = models.ImageField(default='default.png', upload_to = "images/")
    bio = models.TextField(blank=True, null=True)
    fav_exercises = models.TextField(blank=True, null=True)
    objects = UserManager()

    # friend_request = models.ManyToManyField("self") not symmetrical?
    # friend_requests = models.ManyToManyField('self', symmetrical=False, blank=True)
    # sent_friend_requests = models.ManyToManyField('self', symmetrical=False, blank=True, related_name="sent_requests")
    # use many to many for friends, first argument = "self", related_name = "friends", this would be symmetrical?
    friends = models.ManyToManyField('self', blank=True)

    # Space for O2M & M2M Relationships
    # sender in Friend_Request class
    # receiver in Friend_Request class

    # posts > posted_by in Post class
    # liked_posts > liked_by in Post class

    # comments > posted_by in Comment class
    # liked_comments > liked_by in Comment class

    # workouts > created_by in Workout class
    # liked_workouts > liked_by in Workout class

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

class Friend_Request(models.Model):
    sender = models.ForeignKey(User, related_name="sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="receiver", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Sender: {self.sender.username}. Receiver: {self.receiver.username}"

class Workout(models.Model):
    # exercises > workout in Exercise class
    # posts > workout in Post class
    name = models.CharField(max_length=50)
    created_by = models.ForeignKey(User, related_name="workouts", on_delete=models.CASCADE)
    liked_by = models.ManyToManyField(User, related_name="liked_workouts", blank=True)
    objects = WorkoutManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.created_by}/Workout/{self.id}/{self.name}"


class Exercise(models.Model):
    workout = models.ForeignKey(Workout, related_name="exercises", on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    set_count = models.IntegerField()
    rep_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"workout/{self.workout.name}/exercise/{self.id}"

class Post(models.Model):
    content = models.TextField()
    image = models.ImageField(null=True, blank=True, upload_to = "images/")
    posted_by = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    liked_by = models.ManyToManyField(User, related_name="liked_posts", blank=True)
    workout = models.ForeignKey(Workout, null=True, blank=True, related_name="posts", on_delete=models.SET_NULL)
    objects = PostCommentManager()
    # Space for O2M & M2M Relationships
    # comments > post in Comment class

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.posted_by}/Post/{self.id}"

class Comment(models.Model):
    content = models.TextField()
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    posted_by = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    liked_by = models.ManyToManyField(User, related_name="liked_comments", blank=True)
    objects = PostCommentManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.posted_by}/Comment/{self.id}"
