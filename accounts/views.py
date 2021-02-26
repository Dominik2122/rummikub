from django.shortcuts import render
from django.urls import reverse_lazy
from . import forms
from django.views.generic import CreateView
from django.contrib.auth import login, logout
# Create your views here.

class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'signup.html'
