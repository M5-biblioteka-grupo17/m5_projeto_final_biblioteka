from django.urls import path
from . import views

urlpatterns = [
    path("copies/", views.CopiesView.as_view()),
    path("copies/<int:pk>/", views.CopiesDetailView.as_view()),
    path("loan/<int:pk>/", views.LoanView.as_view())
]
