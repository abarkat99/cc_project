from django.contrib.auth.forms import UserChangeForm as AuthUserChangeForm, UserCreationForm as AuthUserCreationForm, UsernameField

from .models import User


class UserChangeForm(AuthUserChangeForm):
    class Meta:
        model = User
        fields = '__all__'
        field_classes = {'username': UsernameField}


class UserCreationForm(AuthUserCreationForm):
    class Meta:
        model = User
        fields = ("username", 'email')
        field_classes = {'username': UsernameField}

