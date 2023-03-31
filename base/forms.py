from django import forms
from .models import User, Topic, Message
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from base.models import Room


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['topic', 'name', 'description', ]
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter your name...'
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'placeholder': 'Write something...'
                }
            )
        }


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.TextInput(
        attrs={
            'type': 'password'
        }
    ))

    class Meta:
        model = User
        fields = ['username', 'password']


class TopicForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = Topic


class CustomUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['full_name',
                  'avatar',
                  'username',
                  'password1',
                  'password2']


class UpdateUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = [
            'full_name',
            'avatar',
            'username',
            'email',
            'bio',
        ]


class MessageForm(forms.ModelForm):
    body = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter your opinion ...'
            }
        )
    )

    class Meta:
        model = Message
        fields = ['body']
