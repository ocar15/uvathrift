from django.urls import path
from . import views

urlpatterns = [
    # path('logout', views.logout, name='logout'),
    path('', views.user_only, name='user_only'),
    path('profile/', views.my_profile, name='my_profile'),
    path('profile/edit', views.edit_profile, name='edit_profile'),
    path('delete', views.delete_profile, name='delete_profile'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('verify-student/', views.request_student_verification, name='request_student_verification'),
    path('verify-student/<str:token>/', views.verify_student_email, name='verify_student_email'),
    path("api/usernames/", views.username_list, name="username_list"),
]