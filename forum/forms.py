from django import forms
from .models import Post, Community, Profile

class CommunityForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = ['name', 'description']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['display_name', 'description']