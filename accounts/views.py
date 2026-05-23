# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            if user:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, '이메일 또는 비밀번호가 틀렸습니다.')
        except User.DoesNotExist:
            messages.error(request, '이메일 또는 비밀번호가 틀렸습니다.')

    return render(request, 'accounts/login.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            messages.error(request, '이미 사용중인 이메일입니다.')
            return render(request, 'accounts/register.html')

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name
        )
        messages.success(request, '회원가입 완료! 로그인해주세요.')
        return redirect('login')

    return render(request, 'accounts/register.html')


def logout_view(request):
    logout(request)
    return redirect('login')