from django.contrib.auth.models import AbstractUser
from django.db import models
class Like(models.Model):
    like = models.IntegerField()
    post_id = models.IntegerField()
    def __str__(self):
        return f"{self.like}"
class User(AbstractUser):
    def __str__(self):
        return f'{self.username}'
class Post(models.Model):
    user = models.CharField(max_length=64)
    content =  models.CharField(max_length=2000)
    time = models.DateTimeField(auto_now_add=True)
    like = models.ForeignKey(Like, on_delete=models.CASCADE, related_name="likes", default=0)
    liked = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liked", default="", blank=True, null=True)
    def __str__(self):
        return f"{self.user}: {self.id}"
    def valid_post(self):
        return len(self.content) > 0 and len(self.user) > 0 and self.like > 0 and len(self.time) > 0
class Follow(models.Model):
    user = models.ForeignKey(User, related_name="user", on_delete=models.CASCADE, unique=False)
    following = models.ManyToManyField(User, related_name="following")