# weddings/views.py
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Wedding, Guestbook
from .forms import WeddingForm, GuestbookForm
from datetime import date


@login_required
def dashboard(request):
    weddings = Wedding.objects.filter(user=request.user)
    form = WeddingForm()
    return render(request, 'weddings/dashboard.html', {
        'weddings': weddings,
        'form': form,
    })


@login_required
def create_wedding(request):
    if request.method == 'POST':
        form = WeddingForm(request.POST, request.FILES)
        if form.is_valid():
            wedding = form.save(commit=False)  # ← 저장 전에 user 먼저 연결
            wedding.user = request.user
            wedding.save()
            messages.success(request, '청첩장이 생성됐어요! 💌')
            return redirect('dashboard')
        else:
            # 폼 유효성 검사 실패시 에러 메시지
            messages.error(request, '입력값을 확인해주세요!')
            weddings = Wedding.objects.filter(user=request.user)
            return render(request, 'weddings/dashboard.html', {
                'weddings': weddings,
                'form': form,
            })
    return redirect('dashboard')


@login_required
def edit_wedding(request, pk):
    wedding = get_object_or_404(Wedding, pk=pk, user=request.user)

    if request.method == 'POST':
        form = WeddingForm(request.POST, request.FILES, instance=wedding)  # ← instance로 기존 데이터 연결
        if form.is_valid():
            form.save()
            messages.success(request, '수정 완료! ✅')
            return redirect('dashboard')
        else:
            messages.error(request, '입력값을 확인해주세요!')
    else:
        form = WeddingForm(instance=wedding)  # ← 기존 데이터 폼에 채워줌

    return render(request, 'weddings/edit.html', {
        'wedding': wedding,
        'form': form,
    })


@login_required
def delete_wedding(request, pk):
    wedding = get_object_or_404(Wedding, pk=pk, user=request.user)
    # ✅ POST 요청일 때만 삭제
    if request.method == 'POST':
        wedding.delete()
        messages.success(request, '삭제됐어요!')
    return redirect('dashboard')

def wedding_page(request, share_code):
    wedding = get_object_or_404(Wedding, share_code=share_code)
    guestbooks = wedding.guestbooks.all()
    today = date.today()
    days_left = (wedding.wedding_date - today).days

    return render(request, 'weddings/wedding_page.html', {
        'wedding': wedding,
        'guestbooks': guestbooks,
        'days_left': days_left,
        'galleries': wedding.get_galleries(),
        'kakao_map_key': os.getenv('KAKAO_MAP_KEY'),
    })


def write_guestbook(request, wedding_id):
    wedding = get_object_or_404(Wedding, pk=wedding_id)
    # ✅ POST 요청일 때만 저장
    if request.method == 'POST':
        form = GuestbookForm(request.POST)
        if form.is_valid():
            guestbook = form.save(commit=False)
            guestbook.wedding = wedding
            guestbook.save()
    return redirect('wedding_page', share_code=wedding.share_code)