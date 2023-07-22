
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="new_post"),
    path("all_posts/<int:page>", views.all_posts, name="all_posts"),
    path("max_page/<str:username>", views.max_page, name="max_page"),
    path("max_page_following", views.max_page_following, name="max_page_following"),
    path("post_view/<int:post_id>", views.post_view, name="post_view"),
    path("post/<int:post_id>", views.post, name="post"),
    path("comments/<int:post_id>/<int:page>", views.comments, name="comments"),
    path("new_comment/<int:post_id>", views.new_comment, name="new_comment"),
    path("max_page_comments/<int:post_id>", views.max_page_comments, name="max_page_comments"),
    path("like/<int:post_id>", views.like, name="like"),
    path("user/<str:username>", views.user, name="user"),
    path("user_posts/<str:username>/<int:page>", views.user_posts, name="user_posts"),
    path("follow", views.follow, name="follow"),
    path("unfollow", views.unfollow, name="unfollow"),
    path("following", views.following, name="following"),
    path("following_posts/<int:page>", views.following_posts, name="following_posts")
]
