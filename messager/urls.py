from django.urls import path, include
from . import views

urlpatterns = [
    path("messages/unarchive/", views.unarchive_messages, name="unarchive_messages"),
    path("messages/undelete/", views.undelete_messages, name="undelete_messages"),
    path("latest-unread/", views.latest_unread_message_api, name="latest-unread-api"),
    path('report/<int:pk>/', views.report_message, name='report_message')
]