from django.urls import path
from . import views

urlpatterns = [
    path("copies/", views.CopiesView.as_view()),
    path("copies/<int:pk>/", views.CopiesDetailView.as_view()),
    path("books/<int:pk>/copies/", views.CopiesListByBookView.as_view()),
    path("loan/copies/<int:pk>/users/<int:id>/", views.LoanView.as_view()),
    path("loan/<int:pk>/return/", views.LoanReturnView.as_view()),
    path("loan/historic/", views.LoanHistoricUserView.as_view()),
    path("loan/users/<int:pk>/historic/", views.LoanHistoricAllUserCollaboratorView.as_view()),
]
