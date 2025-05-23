



"""
URL configuration for optical_character project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from system_management import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('project_management/', include('project_management.urls')),
    path('project_management_api/', include('project_management.api.urls')),
    path('system_management/', include('system_management.urls')),
    path('', views.login_view, name='login'),
    path('system_management_api/', include('system_management.api.urls')),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='system_management/password_management/password_reset.html'),name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='system_management/password_management/password_reset_done.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="system_management/password_management/password_reset_confirm.html"),name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='system_management/password_management/password_reset_complete.html'),name='password_reset_complete')
]
