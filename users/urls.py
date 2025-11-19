from django.urls import path
from . import views

urlpatterns = [
    # path('logout', views.logout, name='logout'),
    path('', views.user_only, name='user_only'),
    path('profile/', views.my_profile, name='my_profile'),
    path('profile/edit', views.edit_profile, name='edit_profile'),
    path('delete', views.delete_profile, name='delete_profile'),
    path('profile/<str:username>/', views.user_profile, name='user_profile')
]