from django.urls import path
from django.contrib.auth import views as auth_views
from .import views

urlpatterns = [
  path('login/', views.login_view, name='login_view'),
  path('otp/', views.otp_views, name='otp_view'),
  path('users/', views.users_view, name='users_view'),
  path('app_dashboard/', views.app_dashboard, name='app_dashboard'),
  path('profile/',views.profile_view, name='profile_view'),
  path('graphs/', views.graphs_view, name='graphs_view'),
  path('logout/', views.logout_view, name='logout_view'),
  path('resend_otp/',views.resend_otp,name='resend_otp'),
  path('user_update_view/',views.user_update_view,name='user_update_view'),
  path('delete_user_view/',views.delete_user_view,name='delete_user_view'),
  path('password_update/', views.password_update, name='password_update'),
  path('keep_session_alive/',views.keep_session_alive,name='keep_session_alive'),

]
