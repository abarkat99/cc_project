from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

from .models import User
from .forms import UserChangeForm, UserCreationForm
# Register your models here.


@admin.register(User)
class UserAdmin(AuthUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
