
from django.contrib import admin
from django.urls import include,path
from django.contrib.auth import views as auth_views
from accounts.views import SignUpView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("pages.urls")),
    path("issues/", include("issues.urls")),
    path("accounts/", include ("accounts.urls")),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path("accounts/", include("django.contrib.auth.urls")),
]

