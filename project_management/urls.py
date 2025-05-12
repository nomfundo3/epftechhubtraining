from django.urls import path
from .import views

urlpatterns = [
    path('create_project_view', views.create_project_view, name='create_project_view'),
    path('update_project_view/', views.update_project_view, name='update_project_view'),
    path('delete_project_view/',views.delete_project_view,name='delete_project_view'),
    path('fetch_user_view/',views.fetch_user_view,name='fetch_user_view'),
    path('create_form_view', views.create_form_view, name='create_form_view'),

    ]
