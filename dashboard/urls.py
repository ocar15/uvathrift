from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path('/items', views.items_list, name='items_list'),
    path('/items/new', views.item_create, name='item_create'),
    path('/cart', views.cart, name='cart'),
    path('/checkout', views.checkout, name='checkout'),
    path('/orders', views.orders, name='orders'),
    path("post/new/", views.create_item, name="item_create"),
    path("post/<int:pk>/delete/", views.delete_item, name="item_delete"),
    path("report-post/<int:pk>/", views.report_post, name='report_post'),
    path("toggle-save-item/<int:pk>/", views.toggle_save_item, name="toggle_save_item"),
    path("saved-items/", views.saved_items, name="saved_items"),
]