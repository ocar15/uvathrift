from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_only, name='admin_only'),
    path('manage-users/', views.manage_users, name='manage_users'),
    path('edit-user/', views.edit_user, name='edit_user'),
    path('manage-posts/', views.manage_posts, name='manage_posts'),
    path('analytics', views.analytics, name='analytics')
]