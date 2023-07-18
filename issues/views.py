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
from django.core.exceptions import PermissionDenied
from accounts.models import Team, CustomUser, Role
from django.shortcuts import get_object_or_404

class IssueDetailView(DetailView):
    template_name = "issues/detail.html"
    model = Issue

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_team = None
        if self.request.user.is_authenticated:
            user_team = self.request.user.team
        
        user_role = None
        if self.request.user.is_authenticated:
            user_role = self.request.user.role

        context['user_team'] = user_team
        context['user_role'] = user_role
        return context


class IssueListView(ListView):
    template_name = "issues/list.html"
    model = Issue

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_team = None
        if self.request.user.is_authenticated:
            user_team = self.request.user.team
        
        user_role = None
        if self.request.user.is_authenticated:
            user_role = self.request.user.role

        context['user_team'] = user_team
        context['user_role'] = user_role
        return context


class IssueUpdateView(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    template_name ="issues/edit.html"
    model = Issue
    fields = ["summary", "description", "priority", "assignee", "status"]
    def form_valid(self, form):
        issue = self.get_object()
        if form.instance.status!=issue.status:
            if self.request.user.role.name !="developer":
                raise PermissionDenied()
                 
        if form.instance.assignee!=issue.assignee:
            if self.request.user.role.name !="scrum master":
                raise PermissionDenied()
            
        return super().form_valid(form)

    def test_func(self):
        team = self.get_object().reporter.team
        return self.request.user.team==team

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add your custom context data here
        user_team = None
        if self.request.user.is_authenticated:
            user_team = self.request.user.team
        
        user_role = None
        if self.request.user.is_authenticated:
            user_role = self.request.user.role

        context['user_team'] = user_team
        context['user_role'] = user_role

        return context


class IssueCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = "issues/new.html"
    model = Issue
    fields = ["summary", "description", "priority", "assignee", "status"]

    def test_func(self):
        po =Role.objects.get(name="product owner")
        return self.request.user.role ==po
    
    def get_initial(self):
        initial = super().get_initial()
        initial["status"] = "to do" 
        return initial
    
    def form_valid(self, form):
        form.instance.reporter = self.request.user
        if not form.cleaned_data["status"]:
            default_status = get_object_or_404(Status, name="to do")
            form.instance.status = default_status
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("list")
    
class IssueDeleteView(
    LoginRequiredMixin, UserPassesTestMixin,DeleteView
):
    template_name ="issues/delete.html"
    model=Issue
    success_url = reverse_lazy("list")

    def test_func(self):
        po =Role.objects.get(name="product owner")

        issue = self.get_object()
        if self.request.user.role==po:
            return True
        return False

   