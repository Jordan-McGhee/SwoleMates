from django.db import models
import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
forbidden_chars = ['@#$%^&*()_+=[{/}\|]?,;:.~`!"']

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

        if len(postData['username']) < 6:
            errors['username'] = "Username must be at least 6 letters long"
        
        for char in forbidden_chars:
            if char in postData['username']:
                errors['username'] = "You used an invalid character. Username can only contain letters and numbers."

        username_unique_check = User.objects.filter(username=postData['username'])

        if username_unique_check:
            errors['username'] = "That username is already taken"

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
            errors['content'] = "Message can't be empty"

        return errors

#  MODELS
class User(models.Model):
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    username = models.CharField(max_length=45, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length = 60)
    profile_photo = models.ImageField(default='default.png', upload_to = "images/")
    objects = UserManager()

    # friend_request = models.ManyToManyField("self") not symmetrical?
    friend_requests = models.ManyToManyField('self', symmetrical=False, blank=True, null=True)
    # use many to many for friends, first argument = "self", related_name = "friends", this would be symmetrical?
    friends = models.ManyToManyField('self', blank=True, null=True)

    # Space for O2M & M2M Relationships
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


class Post(models.Model):
    content = models.TextField()
    image = models.ImageField(null=True, blank=True, upload_to = "images/")
    posted_by = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    liked_by = models.ManyToManyField(User, related_name="liked_posts", blank=True)
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

class Workout(models.Model):
    # exercises > workout in Exercise class
    name = models.CharField(max_length=50)
    created_by = models.ForeignKey(User, related_name="workouts", on_delete=models.CASCADE)
    liked_by = models.ManyToManyField(User, related_name="liked_workouts", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.created_by}/Workout/{self.id}"


class Exercise(models.Model):
    workout = models.ForeignKey(Workout, related_name="exercises", on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    set_count = models.IntegerField()
    rep_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)