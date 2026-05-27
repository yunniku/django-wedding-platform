# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        if not email or not password:
            messages.error(request, '이메일과 비밀번호를 입력해주세요.')
            return render(request, 'accounts/login.html')

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            if user:
                login(request, user)
                # ✅ next 파라미터 처리 (로그인 후 원래 페이지로 이동)
                next_url = request.GET.get('next', 'dashboard')
                return redirect(next_url)
            else:
                messages.error(request, '이메일 또는 비밀번호가 틀렸습니다.')
        except User.DoesNotExist:
            messages.error(request, '이메일 또는 비밀번호가 틀렸습니다.')

    return render(request, 'accounts/login.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        # ✅ 입력값 검증
        if not name:
            messages.error(request, '이름을 입력해주세요.')
            return render(request, 'accounts/register.html')

        if len(password) < 8:
            messages.error(request, '비밀번호는 8자 이상이어야 합니다.')
            return render(request, 'accounts/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, '이미 사용중인 이메일입니다.')
            return render(request, 'accounts/register.html')

        # ✅ 회원가입 후 자동 로그인
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name
        )
        login(request, user)
        messages.success(request, f'{name}님, 환영합니다! 💍')
        return redirect('dashboard')

    return render(request, 'accounts/register.html')


def logout_view(request):
    logout(request)
    return redirect('login')