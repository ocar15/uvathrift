from django.urls import path, include
from .views import inbox

urlpatterns = [
    path("", inbox, name="inbox"),  
]