from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth.models import User
from .models import Post, Comment
from django.core.exceptions import ValidationError
from ckeditor.widgets import CKEditorWidget


class BasicSignupForm(SignupForm):

    first_name = forms.CharField(max_length=100, label='First Name', required=False)
    last_name = forms.CharField(max_length=100, label='Last Name', required=False)
    username = forms.CharField(max_length=100, label='Username', required=False)

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        return user


class UserForm(forms.ModelForm):
   class Meta:
       model = User
       fields = [
           'username',
           'email',
           'first_name',
           'last_name',
       ]

class PostForm(forms.ModelForm):
    class Meta:
       model = Post
       fields = [
           'category',
           'title',
           'content',
       ]

    def clean(self):
       cleaned_data = super().clean()
       return cleaned_data

class CommentForm(forms.ModelForm):

    class Meta:
       model = Comment
       fields = [
           'text',
       ]

    def clean(self):
       cleaned_data = super().clean()
       return cleaned_data
