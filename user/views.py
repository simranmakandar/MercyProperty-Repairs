from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from .forms import *
from .models import *
from django.shortcuts import redirect


class ChangePwView(LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('home')
    template_name = 'registration/change_password.html'


class PwResetView(PasswordResetView):
    form_class = PasswordResetForm
    success_url = reverse_lazy('pw_reset_done')
    template_name = 'registration/pw_reset.html'


class PwResetDoneView(PasswordResetDoneView):
    template_name = 'registration/pw_reset_done.html'


class PwResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy('pw_reset_complete')
    template_name = 'registration/pw_reset_confirm.html'


class PwResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/pw_reset_complete.html'


def signup(request):
    if request.method == 'POST':
        user_form = CreateUserAccountForm(request.POST)
        if user_form.is_valid():
            user_form.save()

            username = user_form.cleaned_data.get('username')
            password = user_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("/")
    else:
        user_form = CreateUserAccountForm()
    return render(request, 'registration/signup.html', {'user_form': user_form})