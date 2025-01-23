from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.all_posts, name='all_posts'),
    path('accounts/', include('allauth.urls')),  # Add this line for allauth
    path('create_community/', views.create_community, name='create_community'),
]