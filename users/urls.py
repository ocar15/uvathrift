from django.urls import path
from . import views

urlpatterns = [
    path("", views.landing_page, name="landing"),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('user/', views.user_only, name='user_only'),
    path('administrator/', views.admin_only, name='admin_only'),
    path('profile/', views.my_profile, name='my_profile'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('items/', views.items_list, name='items_list'),
    path('items/new/', views.item_create, name='item_create'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.orders, name='orders'),
    path('mod/manage-users/', views.manage_users, name='manage_users'),
    path('mod/edit-user/', views.edit_user, name='edit_user')  
]