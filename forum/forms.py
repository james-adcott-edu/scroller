from django import forms
from .models import Post, Community, Profile, Comment

class CommunityForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = ['name', 'description']


class CommunityEditForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = ['description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Edit the community description...'}),
        }
        labels = {
            'description': '',  # Remove the label
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Post title (required)'}),
            'content': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Some text'}),
        }
        labels = {
            'title': '',
            'content': '',
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['display_name', 'description']
        widgets = {
            'display_name': forms.TextInput(attrs={'placeholder': 'display name'}),
            'description': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Bio description'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a comment...'}),
        }
        labels = {
            'content': '',
        }