from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.utils.text import slugify
import shortuuid
from shortuuid.django_fields import ShortUUIDField


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150, blank=True, null=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


    def __str__(self):
        # allows us to use username as a url parameter instead of id
        return self.username


    def save(self, *args, **kwargs):
        user_email, mobile = self.email.split('@')
        # use the first part of the email as the username
        if self.full_name == '' or self.full_name == None:
            self.full_name = user_email
        if self.username == '' or self.username == None:
            self.username = user_email

        super(User, self).save(*args, **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.FileField(upload_to='image/profile', default='default/profile.jpg', blank=True, null=True)
    full_name = models.CharField(max_length=150, blank=True, null=True)
    bio = models.CharField(max_length=400, blank=True, null=True)
    about = models.CharField(max_length=500, blank=True, null=True)
    author = models.BooleanField(default=False)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    whatsapp = models.CharField(max_length=100, blank=True, null=True)
    facebook = models.CharField(max_length=100, blank=True, null=True)
    instagram = models.CharField(max_length=100, blank=True, null=True)
    linkedin = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # allows us to use username as a url parameter instead of id
        return self.user.username


    def save(self, *args, **kwargs):
        if self.full_name == '' or self.full_name == None:
            self.full_name = self.user.full_name

        super(Profile, self).save(*args, **kwargs)


# auto create a profile when a user is created
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


def save_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_profile, sender=User)


# Blog casses

class Category(models.Model):
    title = models.CharField(max_length=100)
    image = models.FileField(upload_to='image/catagory', default='default/catagory.jpg', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = 'Category'

    
    # slugify make the title url friendly like => this is a title -> this-is-a-title
    def save(self, *args, **kwargs):
        if self.slug == "" or self.slug == None:
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    
    def post_count(self):
        return Post.objects.filter(category=self).count()


class Post(models.Model):

    STATUS = (
        ('Active', 'Active'),
        ('Draft', 'Draft'),
        ('Published', 'Published'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=100)
    tags = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    image = models.FileField(upload_to='image/post', default='default/post.jpg', blank=True, null=True)
    status = models.CharField(max_length=100, choices=STATUS, default='Active')
    slug = models.SlugField(unique=True, blank=True, null=True)
    view = models.IntegerField(default=0)
    like = models.ManyToManyField(User, related_name='likes_by_user', blank=True)
    date = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Post'
    
    def save(self, *args, **kwargs):
        if self.slug == "" or self.slug == None:
            self.slug = slugify(self.title) + '-' + shortuuid.uuid()[:2]
            # this prevents the slug conflict in the case of same title from different users as slug is unique
            # this will add a random 2 character string to the end of the slug like => this-is-a-title-12
        super(Post, self).save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(null=True, blank=True)
    # the 'self' is used to make the reply recursive
    reply = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.post.title
    
    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Comment'

    
class Bookmark(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.post.title
    
    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Bookmark'


class Notification(models.Model):
    NOTIFICATION_TYPE = (
        ('Like', 'Like'),
        ('Comment', 'Comment'),
        ('Reply', 'Reply'),
        ('Bookmark', 'Bookmark'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    type = models.CharField(max_length=100, choices=NOTIFICATION_TYPE)
    seen = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        if self.post:
            return f"{self.type}- {self.post.title}"
        else:
            return "Notification"
        
    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Notification'
