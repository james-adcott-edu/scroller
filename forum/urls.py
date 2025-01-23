from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.all_posts, name='all_posts'),
    path('accounts/', include('allauth.urls')),  # Add this line for allauth
    path('create_community/', views.create_community, name='create_community'),
    path('community/<slug:slug>/', views.community_detail, name='community_detail'),
    path('community/<slug:community_slug>/<int:post_id>/', views.post_detail, name='post_detail'),
]