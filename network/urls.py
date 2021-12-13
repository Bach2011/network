
from django.db.models.fields import related
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:username>", views.profile, name="profile"),
    #API
    path("like/<int:id>", views.like, name="like"),
    path("follow", views.follow, name="follow")
]
