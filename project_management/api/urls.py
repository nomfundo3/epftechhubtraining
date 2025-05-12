from django.urls import path
from project_management.api import views

urlpatterns = [
    path('create_project_api_get/',views.create_project_api_get,name='create_project_api_get'),
    path('create_project_api_post/', views.create_project_api_post, name='create_project_api_post'),
    path('update_project_api/', views.update_project_api, name='update_project_api'),
    path('delete_project_api/',views.delete_project_api,name='delete_project_api'),
    path('fetch_user_api/',views.fetch_user_api,name='fetch_user_api'),
    path('create_form_api/', views.create_form_api, name='create_form_api'),


]