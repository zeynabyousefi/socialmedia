from django.contrib import admin
from .models import PostUser, CommentPost

# Register your models here.
admin.site.register(PostUser)
admin.site.register(CommentPost)
