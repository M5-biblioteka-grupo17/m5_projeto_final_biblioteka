from django.urls import path
from . import views

urlpatterns = [
    path("books/<pk>/", views.BookDetailView.as_view()),
    path("books/<pk>/follow/", views.BookFollowView.as_view()),
    path("books/<pk>/unfollow/", views.BookUnfollowView.as_view())
]
