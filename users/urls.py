from django.urls import path
from . import views

urlpatterns = [
    path("", views.landing_page, name="landing"),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
]