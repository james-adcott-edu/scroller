from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import CommunityForm, PostForm, ProfileForm, CommentForm, CommunityEditForm
from .models import Community, Post, Profile, Comment
from django.contrib import messages



def is_admin(user):
    return user.is_staff


@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, "Your account has been deleted successfully.")
        return redirect('home')
    return render(request, 'delete_account.html')
    

def all_posts(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'all_posts.html', {'posts': posts, 'title': 'All Posts'})


def home(request):
    if request.user.is_authenticated:
        # Get the communities the user is subscribed to
        communities = request.user.subscribed_communities.all()
        
        # Get the users the user is subscribed to
        subscribed_profiles = request.user.subscribed_users.all()
        
        # Get the users from the subscribed profiles
        subscribed_users = User.objects.filter(profile__in=subscribed_profiles)
        
        # Get posts from subscribed communities
        community_posts = Post.objects.filter(community__in=communities).order_by('-created_at')
        
        # Get posts from subscribed user profiles with no community
        user_posts = Post.objects.filter(community__isnull=True, created_by__in=subscribed_users).order_by('-created_at')
        
        # Combine the two querysets
        posts = community_posts | user_posts
        posts = posts.distinct().order_by('-created_at')
        context = {
            'subscribed_communities': communities,
            'subscribed_profiles': subscribed_profiles,
            'posts': posts
        }
    else:
        context = {
            'posts': Post.objects.all().order_by('-created_at'),
        }
    
    return render(request, 'home.html', context)

def subscriptions(request):
    if request.user.is_authenticated:
        # Get the communities the user is subscribed to
        subscribed_communities = request.user.subscribed_communities.all()
        
        # Get the profiles the user is subscribed to
        subscribed_profiles = request.user.subscribed_users.all()
        
        context = {
            'subscribed_communities': subscribed_communities,
            'subscribed_profiles': subscribed_profiles,
        }
    else:
        context = {
            'subscribed_communities': [],
            'subscribed_profiles': [],
        }
    
    return render(request, 'subscriptions.html', context)


def community_list(request):
    communities = Community.objects.all()
    return render(request, 'community_list.html', {'communities': communities})


def subscribe_profile(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    if request.user.is_authenticated:
        profile.subscribers.add(request.user)
        profile.save()
        return render(request, 'subscription_button.html', {'user': request.user, 'profile':profile})
    return redirect('login')

def unsubscribe_profile(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    if request.user.is_authenticated:
        profile.subscribers.remove(request.user)
        profile.save()
        return render(request, 'subscription_button.html', {'user': request.user, 'profile':profile})
    return redirect('login')


def subscribe(request, slug):
    community = get_object_or_404(Community, slug=slug)
    if request.user.is_authenticated:
        community.subscribers.add(request.user)
        community.save()
        return render(request, 'community_subscription_button.html', {'user': request.user, 'community': community})
    return redirect('login')

def unsubscribe(request, slug):
    community = get_object_or_404(Community, slug=slug)
    if request.user.is_authenticated:
        community.subscribers.remove(request.user)
        community.save()
        return render(request, 'community_subscription_button.html', {'user': request.user, 'community': community})
    return redirect('login')

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
                return redirect('community_detail', community.name)
    else:
        form = CommunityForm()
    
    return render(request, 'create_community.html', {'form': form})


@login_required
def edit_community(request, slug):
    community = get_object_or_404(Community, slug=slug)
    
    # Check if the current user is the creator of the community
    if request.user != community.created_by and is_admin(request.user) == False:
        return redirect('community_detail', slug=community.slug)

    if request.method == 'POST':
        form = CommunityEditForm(request.POST, instance=community)
        if form.is_valid():
            form.save()
            return redirect('community_detail', slug=community.slug)
    else:
        form = CommunityEditForm(instance=community)

    return render(request, 'edit_community.html', {'form': form, 'community': community})


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
                if request.htmx:
                    return render(request, 'comment.html', {'comment': comment, 'post': post, 'form': CommentForm()})
                return redirect('post_detail', community_slug=community.slug, post_id=post.id)
        else:
            return redirect('account_login')
    else:
        form = CommentForm()

    return render(request, 'post_detail.html', {'post': post, 'comments': comments, 'form': form})


def comment_partial(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    return render(request, 'comment.html', {'comment': comment, 'post':comment.post})


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, created_by=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            if post.community:
                return redirect('post_detail', community_slug=post.community.slug, post_id=post.id)
            return redirect('user_post_detail',  username=post.created_by.username, post_id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'edit_post.html', {'form': form, 'post': post})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, created_by=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('home')
    return render(request, 'delete_post.html', {'post': post})

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user != comment.created_by and not request.user.is_staff:
        if comment.post.community:
            return redirect('post_detail', community_slug=comment.post.community.slug, post_id=comment.post.id)
        return redirect('user_post_detail',  username=comment.post.created_by.username, post_id=comment.post.id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            if comment.post.community:
                return redirect('post_detail', community_slug=comment.post.community.slug, post_id=comment.post.id)
            return redirect('user_post_detail',  username=comment.post.created_by.username, post_id=comment.post.id)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'edit_comment.html', {'form': form, 'comment': comment})

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user != comment.created_by and not request.user.is_staff:
        if comment.post.community:
            return redirect('post_detail', community_slug=comment.post.community.slug, post_id=comment.post.id)
        return redirect('user_post_detail',  username=comment.post.created_by.username, post_id=comment.post.id)

    if request.method == 'POST':
        comment.delete()
        if comment.post.community:
            return redirect('post_detail', community_slug=comment.post.community.slug, post_id=comment.post.id)
        return redirect('user_post_detail',  username=comment.post.created_by.username, post_id=comment.post.id)

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
                if request.htmx:
                    return render(request, 'comment.html', {'comment': comment, 'post': post, 'form': CommentForm()})
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