
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following", views.following, name="following"),

    # API Routes
    path("posts/submit", views.submit_post, name="submit_post"),
    path("posts/<str:postbox>", views.show_posts, name="show_post")
]
