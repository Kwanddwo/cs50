
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="new_post"),
    path("all_posts/<int:page>", views.all_posts, name="all_posts"),
    path("max_page", views.max_page, name="max_page"),
    path("comments/<int:post_id>", views.comments, name="comments"),
    path("like/<int:post_id>", views.like, name="like"),
    path("user/<str:username>", views.user, name="user"),
    path("user_posts/<str:username>/<int:page>", views.user_posts, name="user_posts"),
    path("follow/<str:username>", views.follow, name="follow"),
    path("unfollow/<str:username>", views.unfollow, name="unfollow")
]
