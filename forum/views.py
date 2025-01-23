from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CommunityForm
from .models import Community, Post

def all_posts(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'all_posts.html', {'posts': posts})


@login_required
def create_community(request):
    if request.method == 'POST':
        form = CommunityForm(request.POST)
        if form.is_valid():
            community_name = form.cleaned_data['name']
            if Community.objects.filter(name=community_name).exists():
                # Community with this name already exists
                error_message = f"A community with the name '{community_name}' already exists."
                return render(request, 'create_community.html', {'form': form, 'error_message': error_message})
            else:
                community = form.save(commit=False)
                community.created_by = request.user
                community.save()
                return redirect('community_detail', community.id)
    else:
        form = CommunityForm()
    
    return render(request, 'create_community.html', {'form': form})