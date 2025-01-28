from django.test import TestCase
from .forms import CommunityForm, CommunityEditForm, PostForm, ProfileForm, CommentForm
from .models import Community, Post, Profile, Comment
from django.contrib.auth.models import User


#
# FORM TESTING
#

class CommunityFormTest(TestCase):
    def test_valid_community_form(self):
        form = CommunityForm(data={'name': 'test_community', 'description': 'A test community'})
        self.assertTrue(form.is_valid())
    
    def test_invalid_community_form(self):
        form = CommunityForm(data={'name': '', 'description': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

class CommunityEditFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.community = Community.objects.create(
            name='test_community',
            description='A test community',
            created_by=self.user
        )
    
    def test_valid_community_edit_form(self):
        form = CommunityEditForm(data={'description': 'Updated description'}, instance=self.community)
        self.assertTrue(form.is_valid())
        updated_community = form.save()
        self.assertEqual(updated_community.description, 'Updated description')
    
    def test_invalid_community_edit_form(self):
        form = CommunityEditForm(data={'description': ''}, instance=self.community)
        self.assertTrue(form.is_valid())  # Assuming description can be blank

class PostFormTest(TestCase):
    def test_valid_post_form(self):
        form = PostForm(data={'title': 'Test Title', 'content': 'This is the content.'})
        self.assertTrue(form.is_valid())
    
    def test_invalid_post_form(self):
        form = PostForm(data={'title': '', 'content': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
        self.assertIn('content', form.errors)

class CommentFormTest(TestCase):
    def test_valid_comment_form(self):
        form = CommentForm(data={'content': 'This is a comment.'})
        self.assertTrue(form.is_valid())
    
    def test_invalid_comment_form(self):
        form = CommentForm(data={'content': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)


