from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from .models import Task


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']


class RegisterForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', max_length=100, widget=forms.PasswordInput)
