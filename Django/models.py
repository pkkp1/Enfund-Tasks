from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    bio = models.TextField()

class BlogPost(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()

class Tag(models.Model):
    name = models.CharField(max_length=50)
    posts = models.ManyToManyField(BlogPost, related_name='tags')