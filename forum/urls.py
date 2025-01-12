from django.urls import path
from .views import Posts

urlpatterns = [
    path('', Posts)
]