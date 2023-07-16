from django.urls import path
from . import views

urlpatterns = [
path("", views.IssueListView.as_view(), name="list"),
path("<int:pk>/", views.IssueDetailView.as_view(), name="detail"),
path("new/", views.IssueCreateView.as_view(), name="new"), 
]