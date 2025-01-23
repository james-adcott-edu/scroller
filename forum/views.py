from django.shortcuts import render
from .models import Post

def all_posts(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'all_posts.html', {'posts': posts})