from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import render, redirect

from .forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class UserLoginView(LoginView):
    template_name = "accounts/login.html"
    fields = ("username", "password")
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("todo:task_list")


class UserRegisterView(View):
    template_name = "accounts/register.html"
    form_class = UserCreationForm

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['email'],
                                     cd['password1'])

            return redirect('todo:task_list')
        else:
            return render(request, self.template_name, {'form': form})








class UserLogoutView(LoginRequiredMixin,View):
    def get(self, request):
        logout(request)
        return redirect(reverse_lazy('accounts:user_login'))
