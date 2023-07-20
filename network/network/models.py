from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    bio = models.TextField(max_length=200)

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('follower', 'followed', ), name="follow_unique")
        ]

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self, user=None):
        return {
            "id": self.id,
            "user": self.user.username,
            "text": self.text,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "like_count": self.likes.count(),
            "liked": Like.objects.filter(user=user, post=self).exists()
        }
    
    def __str__(self):
        return f"{self.user} posted {self.text} on {self.timestamp}"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")

    class Meta:
        unique_together = ('user', 'post',)

    def __str__(self):
        return f"{self.user} liked {self.post}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "text": self.text,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p")
        }
    
    def __str__(self):
        return f"{self.user} commented {self.text} on post with id {self.post.pk} on {self.timestamp}"
