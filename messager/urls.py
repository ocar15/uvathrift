from django.urls import path, include
from . import views

urlpatterns = [
    path("messages/unarchive/", views.unarchive_messages, name="unarchive_messages"),
    path("messages/undelete/", views.undelete_messages, name="undelete_messages"),

]