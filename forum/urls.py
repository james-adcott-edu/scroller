from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('all/', views.all_posts, name='all_posts'),  # All posts
    path('accounts/', include('allauth.urls')),  # Add this line for allauth
    path('create_community/', views.create_community, name='create_community'),
    path('community/<slug:slug>/', views.community_detail, name='community_detail'),
    path('community/<slug:community_slug>/<int:post_id>/', views.post_detail, name='post_detail'),
    path('profile/<str:username>/', views.profile_view, name='profile_view'),  # Profile view
    path('editprofile', views.edit_profile, name='edit_profile'),  # Edit profile
    path('comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),  # Edit comment
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),  # Delete comment
]