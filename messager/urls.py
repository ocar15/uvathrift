from django.urls import path, include
from . import views

urlpatterns = [
    path("messages/unarchive/", views.unarchive_messages, name="unarchive_messages"),
    path("messages/undelete/", views.undelete_messages, name="undelete_messages"),
    path("latest-unread/", views.latest_unread_message_api, name="latest-unread-api"),
    path('report/<int:pk>/', views.report_message, name='report_message'),
    path('groups/', views.group_list, name="group_list"),
    path("groups/create/", views.create_group, name='create_group'),
    path('groups/<int:group_id>/', views.group_detail, name='group_detail'),
    path("groups/<int:group_id>/send", views.send_group_message, name='send_group_message'),
    path("groups/delete_group/<int:group_id>", views.delete_group, name="delete_group"),
    path("groups/leave_group/<int:group_id>", views.leave_group, name="leave_group"),
]