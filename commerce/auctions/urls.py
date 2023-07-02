from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<int:listing_index>", views.listing, name="listing"),
    path("listing/create", views.create_listing, name="create_listing"),
    path("listing/<int:listing_index>/bid", views.bid, name="bid"),
    path("user/<str:username>", views.user_view, name="user_view"),
    path("listing/<int:listing_index>/close", views.close, name="close"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("listing/<int:listing_id>/comment", views.comment, name="comment"),
    path("categories", views.categories, name="categories")
]
