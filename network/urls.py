
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following", views.following, name="following"),
    path("user/<str:username>", views.userPage, name="userPage"),

    # API Routes
    path("posts/submit", views.submit_post, name="submit_post"),
    path("posts/<str:postbox>", views.show_posts, name="show_post"),
    path("follow/<str:userID>", views.follow, name="follow"),
    path("like/<int:postID>", views.like, name="like"),
    path("like/count/<int:postID>", views.like_count, name="like"),
    path("like/countnotloggin/<int:postID>",
         views.like_count_notloggin, name="like"),
    path("edit/<int:postID>", views.editPost, name="infoEditPost"),
    path("edit/submit", views.editPostInDB, name="editPost")
]
