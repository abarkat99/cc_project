from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from .forms import UserCreationForm
from django.views.generic import FormView, UpdateView
from django.contrib.auth import login
from django.urls import reverse_lazy

from .models import User
# Create your views here.


class SignupView(FormView):
    form_class = UserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email',)
    template_name = 'my_account.html'
    success_url = reverse_lazy('my_account')

    def get_object(self, queryset=None):
        return self.request.user
