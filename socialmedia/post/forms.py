from django import forms
from .models import PostUser, CommentPost


class CreatePost(forms.ModelForm):
    class Meta:
        model = PostUser
        fields = ('body', 'img',)


class CreateComment(forms.ModelForm):
    class Meta:
        model = CommentPost
        fields = ('body', )
