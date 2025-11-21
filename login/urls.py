from django.urls import path
from . import views

urlpatterns = [
    path("", views.landing_page, name="landing"),
    path("suspended/", views.suspended, name='suspended'),
    path('appeal/', views.appeal, name='appeal'),
    path("logout/", views.logout, name='logout')
]