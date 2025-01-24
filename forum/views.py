from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import CommunityForm, PostForm, ProfileForm, CommentForm
from .models import Community, Post, Profile, Comment



def is_admin(user):
    return user.is_staff
    

def all_posts(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'all_posts.html', {'posts': posts})

def home(request):
    if request.user.is_authenticated:
        communities = request.user.subscribed_communities.all()
        posts = Post.objects.filter(community__in=communities).order_by('-created_at')
    else:
        posts = Post.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'posts': posts})


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


def community_detail(request, slug):
    community = get_object_or_404(Community, slug=slug)
    posts = Post.objects.filter(community=community).order_by('-created_at')
    is_subscribed = False
    if request.user.is_authenticated:
        is_subscribed = community.subscribers.filter(id=request.user.id).exists()

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.created_by = request.user
                post.community = community
                post.save()
                return redirect('community_detail', slug=community.slug)
        else:
            return redirect('account_login')
    else:
        form = PostForm()

    return render(request, 'community_detail.html', {'community': community, 'posts': posts, 'form': form, 'is_subscribed': is_subscribed})


@login_required
def subscribe(request, slug):
    community = get_object_or_404(Community, slug=slug)
    community.subscribers.add(request.user)
    return redirect('community_detail', slug=slug)

@login_required
def unsubscribe(request, slug):
    community = get_object_or_404(Community, slug=slug)
    community.subscribers.remove(request.user)
    return redirect('community_detail', slug=slug)



def post_detail(request, community_slug, post_id):
    community = get_object_or_404(Community, slug=community_slug)
    post = get_object_or_404(Post, pk=post_id, community=community)
    comments = post.comments.filter(parent_comment__isnull=True).order_by('-created_at')
    
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.created_by = request.user
                parent_id = request.POST.get('parent_id')
                if parent_id:
                    comment.parent_comment = Comment.objects.get(id=parent_id)
                comment.save()
                return redirect('post_detail', community_slug=community.slug, post_id=post.id)
        else:
            return redirect('account_login')
    else:
        form = CommentForm()

    return render(request, 'post_detail.html', {'post': post, 'comments': comments, 'form': form})

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user != comment.created_by and not request.user.is_staff:
        return redirect('post_detail', community_slug=comment.post.community.slug, post_id=comment.post.id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post_detail', community_slug=comment.post.community.slug, post_id=comment.post.id)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'edit_comment.html', {'form': form, 'comment': comment})

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user != comment.created_by and not request.user.is_staff:
        return redirect('post_detail', community_slug=comment.post.community.slug, post_id=comment.post.id)

    if request.method == 'POST':
        comment.delete()
        return redirect('post_detail', community_slug=comment.post.community.slug, post_id=comment.post.id)

    return render(request, 'delete_comment.html', {'comment': comment})


def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile
    posts = Post.objects.filter(created_by=user).order_by('-created_at')

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.created_by = request.user
                post.save()
                return redirect('profile_view', username=username)
    else:
        form = PostForm()

    return render(request, 'profile.html', {'profile': profile, 'posts': posts, 'form': form})


def user_post_detail(request, username, post_id):
    user = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, id=post_id, created_by=user, community__isnull=True)
    comments = post.comments.filter(parent_comment__isnull=True).order_by('-created_at')
    
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.created_by = request.user
                parent_id = request.POST.get('parent_id')
                if parent_id:
                    comment.parent_comment = Comment.objects.get(id=parent_id)
                comment.save()
                return redirect('user_post_detail', username=username, post_id=post.id)
        else:
            return redirect('account_login')
    else:
        form = CommentForm()

    return render(request, 'user_post_detail.html', {'post': post, 'comments': comments, 'form': form})
    

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile_view', username=request.user.username)
    else:
        form = ProfileForm(instance=request.user.profile)

    return render(request, 'edit_profile.html', {'form': form})