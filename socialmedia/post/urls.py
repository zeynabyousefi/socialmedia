from django.urls import path
from .views import *

urlpatterns = [
    path('posts/', PostView.as_view(), name="post_view"),
    path('post/<int:post_id>/<slug:slug>/', PostDetail.as_view(), name="post_detail"),
    path('create/', PostCreate.as_view(), name="post_create"),
    path('delete/<int:post_id>/', PostDelete.as_view(), name="post_delete"),
    path('recently/', PostRecently.as_view(), name="post_recently"),
    path('edit/<int:post_id>', Update.as_view(), name="post_update"),
    # path('comment/', CreateCommentForm.as_view(), name="comment"),

]
