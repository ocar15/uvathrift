from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.inbox, name="inbox"),
    path("", views.sent, name="sent"),
    path("", views.view, name="view"),
    path("", views.write, name="write"),
]