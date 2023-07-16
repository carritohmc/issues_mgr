from typing import Any, Dict, Optional
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    DeleteView,
    UpdateView
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from django.urls import reverse_lazy
from .models import Issue, Status, Priority
from accounts.models import Role

class IssueDetailView(DetailView):
    template_name = "issues/detail.html"
    model = Issue

class IssueListView(ListView):
    template_name = "issues/list.html"
    model = Issue

class IssueUpdateView(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    template_name ="issues/edit.html"
    model = Issue
    fields = ["summary", "description", "priority", "assignee"]

class IssueCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = "issues/new.html"
    model = Issue
    fields = ["summary", "description", "priority", "assignee"]

    def test_func(self):
        po =Role.objects.get(name="product owner")
        return self.request.user.role ==po
    
    def get_initial(self):
        initial = super().get_initial()
        initial["status"] = "to do" 
        return initial
    
class IssueDeleteView(
    LoginRequiredMixin, UserPassesTestMixin,DeleteView
):
    template_name ="issues/delete.html"
    modle=Issue

    def test_func(self):
        po =Role.objects.get(name="product owner")
        done_status = Status.objects.get(name="done")
        issue = self.get_object()
        if issue.status == done_status and self.request.user.role==po:
            return True
        return False

   