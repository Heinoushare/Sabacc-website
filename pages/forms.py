from django.contrib.auth.forms import UserCreationForm

from .models import Chat

from django import forms

from django.contrib.auth.models import User

class CreateUserForm(UserCreationForm):
  class Meta:
    model = User
    fields = [
      'username', 'email', 'password1', 'password2'
    ]

class ChatForm(forms.ModelForm):
  class Meta:
    model = Chat
    fields = [
      'message'
    ]