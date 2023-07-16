
from django.contrib import admin
from django.urls import include,path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("pages.urls")),
    path("issues/", include("issues.urls")),
    path("accounts/", include ("accounts.urls")),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('signup/', auth_views.LoginView.as_view(template_name='registration/signup.html'), name='signup'),
]
