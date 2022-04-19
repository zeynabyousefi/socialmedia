from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from post.models import PostUser
from .models import Relation


class UserRegisterView(View):
    form_class = UserRegisterForm
    template_name = 'user/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'], cd['email'], cd['password_01'])
            messages.success(request, 'you registered successfully ')
            return redirect('home')
        return render(request, self.template_name, {'form': form})


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'user/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd["username"], password=cd['password'], email=cd['email'])
            if user is not None:
                login(request, user)
                messages.success(request, 'you logged successfully ', 'success')
                return redirect('home')
            messages.error(request, "user name or password is wrong", 'warning')
        return render(request, self.template_name, {"form": form})


class UserLogoutView(LoginRequiredMixin, View):
    # login_url = '/user/login/'

    def get(self, request):
        logout(request)
        messages.success(request, 'you logout successfully', 'success')
        return redirect('home')


class UserProfileView(LoginRequiredMixin, View):
    template = 'user/profile.html'

    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        post = PostUser.objects.filter(user=user)
        return render(request, self.template, {'user': user, 'post': post})


class UserFollow(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exist():
            messages.error(request,'you are already following this user','danger')


class UserUnfollow(LoginRequiredMixin, View):
    pass
