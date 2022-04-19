from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from .managers import RecentlyPostManager


class PostUser(models.Model):
    body = models.TextField()
    slug = models.SlugField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    img = models.ImageField(upload_to='images/', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = RecentlyPostManager()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.slug}-{self.updated}'


class CommentPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment')
    post = models.ForeignKey(PostUser, on_delete=models.CASCADE, related_name='post_comment')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
