from django.urls import path
from system_management.api import views

urlpatterns = [
    path('api_login/', views.login_view, name='login'),
    path('otp_verify/',views.verify_otp, name='otp_verify'),
    path('profile_api/',views.profile_api, name='profile_api'),
    path('api_logout/', views.logout_view, name='logout'),
    path('users_api_get/',views.users_api_get,name='users_api_get'),
    path('users_api_post/',views.users_api_post,name='users_api_post'),
    path('resend_otp_api/',views.resend_otp_api,name='resend_otp_api'), 
    path('resend_otp_api/',views.resend_otp_api,name='resend_otp_api'),
    path('delete_user_api/',views.delete_user_api,name='delete_user_api'),
    path('update_user_api/',views.update_user_api,name='update_user_api'),
    path('update_password_api/',views.update_password_api,name='update_password_api'),
    path('dashboard_api/',views.dashboard_api,name='dashboard_api'),
    
]
