from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
        }

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Post")
    body = models.TextField(blank=True)
    archived = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def serialize(self):
        return {
            "id": self.id,
            "body": self.body,
            "user": self.user.username,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p")
        }
        
class LikePost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="LikeUser")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="PostLiked")
    like = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def serialize(self):
        return {
            "id": self.id,
            "post": self.post,
            "user": self.user,
            "like": self.like,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p")
        }
        
class CommentPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="CommentUser")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="Postcommented")
    comment = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def serialize(self):
        return {
            "id": self.id,
            "post": self.post,
            "user": self.user,
            "comment": self.comment,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p")
        }