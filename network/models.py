from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.CharField(max_length=64)
    content =  models.CharField(max_length=2000)
    time = models.DateTimeField(auto_now_add=True)
    like = models.IntegerField()
    def __str__(self):
        return f"{self.user}: {self.content}"

class Comment(models.Model):
    content = models.CharField(max_length=200)
    user = models.CharField(max_length=64)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post")
    time = models.TimeField(auto_now_add=True)
