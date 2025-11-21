from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_only, name='admin_only'),
    path('manage-users/', views.manage_users, name='manage_users'),
    path('manage-appeals/', views.manage_appeals, name='manage_appeals'),
    path('view-appeal/', views.view_appeal, name='view_appeal'),
    path('edit-user/', views.edit_user, name='edit_user'),
    path('manage-posts/', views.manage_posts, name='manage_posts'),
    path('analytics', views.analytics, name='analytics')
]