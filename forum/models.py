from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from django.core.validators import RegexValidator, MaxLengthValidator


class Community(models.Model):
    name = models.CharField(
        max_length=25,
        unique=True,
        validators=[
            RegexValidator(
                regex='^[a-z_]+$',
                message='Community name must be lowercase ASCII letters and underscores only.',
                code='invalid_name'
            ),
            MaxLengthValidator(25)
        ]
    )
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='communities')
    subscribers = models.ManyToManyField(User, related_name='subscribed_communities', blank=True)
    slug = models.SlugField(unique=True, max_length=25, blank=True)

    @property
    def rendered_description(self):
        from .utils import render_markdown
        return render_markdown(self.description)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    community = models.ForeignKey(Community, null=True, blank=True, on_delete=models.CASCADE, related_name='posts')
    upvotes = models.ManyToManyField(User, related_name='upvoted_posts', blank=True)
    downvotes = models.ManyToManyField(User, related_name='downvoted_posts', blank=True)

    @property
    def rendered_content(self):
        from .utils import render_markdown
        return render_markdown(self.content)

    def score(self):
        return self.upvotes.count() - self.downvotes.count()

    def __str__(self):
        return self.title

    def comment_count(self):
        return self.comments.count()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    upvotes = models.ManyToManyField(User, related_name='upvoted_comments', blank=True)
    downvotes = models.ManyToManyField(User, related_name='downvoted_comments', blank=True)

    @property
    def rendered_content(self):
        from .utils import render_markdown
        return render_markdown(self.content)

    def score(self):
        return self.upvotes.count() - self.downvotes.count()

    def __str__(self):
        return f'Comment by {self.created_by.username} on {self.post.title}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    subscribers = models.ManyToManyField(User, related_name='subscribed_users', blank=True)


    @property
    def rendered_description(self):
        from .utils import render_markdown
        return render_markdown(self.description)
    
    def __str__(self):
        return self.user.username

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

from django.db.models.signals import post_save
post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)