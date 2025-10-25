from django.urls import path
from . import views

urlpatterns = [
    path('', views.messages_overview, name='messages_overview'),
]