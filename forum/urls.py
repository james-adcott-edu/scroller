from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('all/', views.all_posts, name='all_posts'),  # All posts
    path('accounts/', include('allauth.urls')),  # Add this line for allauth
    path('create_community/', views.create_community, name='create_community'),
    path('c/<slug:slug>/', views.community_detail, name='community_detail'),
    path('c/<slug:community_slug>/<int:post_id>/', views.post_detail, name='post_detail'),
    path('u/<str:username>/', views.profile_view, name='profile_view'),  # Profile view
    path('u/<str:username>/<int:post_id>/', views.user_post_detail, name='user_post_detail'),  # User post detail
    path('editprofile', views.edit_profile, name='edit_profile'),  # Edit profile
    path('post/<int:post_id>/edit/', views.edit_post, name='edit_post'),   # Edit post
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),   # Delete post
    path('comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),  # Edit comment
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),  # Delete comment
    path('comment/<int:comment_id>/', views.comment_partial, name='comment_partial'), # Comment Partial
    path('c/<slug:slug>/subscribe/', views.subscribe, name='subscribe'),  # Subscribe to community
    path('c/<slug:slug>/unsubscribe/', views.unsubscribe, name='unsubscribe'),  # Unsubscribe from community
    path('profile/<int:profile_id>/subscribe/', views.subscribe_profile, name='subscribe_profile'),
    path('profile/<int:profile_id>/unsubscribe/', views.unsubscribe_profile, name='unsubscribe_profile'),
    path('subscriptions/', views.subscriptions, name='subscriptions'),  # List subscriptions
]