# weddings/views.py
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Wedding, Guestbook
from datetime import date

@login_required
def dashboard(request):
    weddings = Wedding.objects.filter(user=request.user)
    return render(request, 'weddings/dashboard.html', {'weddings': weddings})

@login_required
def create_wedding(request):
    if request.method == 'POST':
        wedding = Wedding(user=request.user)
        wedding.groom_name = request.POST.get('groom_name')
        wedding.bride_name = request.POST.get('bride_name')
        wedding.wedding_date = request.POST.get('wedding_date')
        wedding.venue = request.POST.get('venue')
        wedding.venue2 = request.POST.get('venue2', '')
        wedding.message = request.POST.get('message', '')
        wedding.groom_phone = request.POST.get('groom_phone', '')
        wedding.bride_phone = request.POST.get('bride_phone', '')
        wedding.groom_account = request.POST.get('groom_account', '')
        wedding.bride_account = request.POST.get('bride_account', '')
        wedding.map_url = request.POST.get('map_url', '')
        wedding.theme = request.POST.get('theme', 'classic')
        wedding.photo_orientation = request.POST.get('photo_orientation', 'landscape')

        if 'photo' in request.FILES:
            wedding.photo = request.FILES['photo']

        gallery_files = request.FILES.getlist('gallery_files')
        for i, file in enumerate(gallery_files[:8], start=1):
            setattr(wedding, f'gallery{i}', file)


        wedding.save()
        messages.success(request, '청첩장이 생성됐어요! 💌')
        return redirect('dashboard')

    return render(request, 'weddings/dashboard.html')

@login_required
def edit_wedding(request, pk):
    wedding = get_object_or_404(Wedding, pk=pk, user=request.user)

    if request.method == 'POST':
        wedding.groom_name = request.POST.get('groom_name')
        wedding.bride_name = request.POST.get('bride_name')
        wedding.wedding_date = request.POST.get('wedding_date')
        wedding.venue = request.POST.get('venue')
        wedding.venue2 = request.POST.get('venue2', '')
        wedding.message = request.POST.get('message', '')
        wedding.groom_phone = request.POST.get('groom_phone', '')
        wedding.bride_phone = request.POST.get('bride_phone', '')
        wedding.groom_account = request.POST.get('groom_account', '')
        wedding.bride_account = request.POST.get('bride_account', '')
        wedding.map_url = request.POST.get('map_url', '')
        wedding.theme = request.POST.get('theme', 'classic')
        wedding.photo_orientation = request.POST.get('photo_orientation', 'landscape')

        if 'photo' in request.FILES:
            wedding.photo = request.FILES['photo']

        gallery_files = request.FILES.getlist('gallery_files')
        for i, file in enumerate(gallery_files[:8], start=1):
            setattr(wedding, f'gallery{i}', file)

        wedding.save()
        messages.success(request, '수정 완료! ✅')
        return redirect('dashboard')

    return render(request, 'weddings/edit.html', {'wedding': wedding})

@login_required
def delete_wedding(request, pk):
    wedding = get_object_or_404(Wedding, pk=pk, user=request.user)
    wedding.delete()
    messages.success(request, '삭제됐어요!')
    return redirect('dashboard')

def wedding_page(request, share_code):
    wedding = get_object_or_404(Wedding, share_code=share_code)
    guestbooks = wedding.guestbooks.all()

    # D-day 계산
    today = date.today()
    days_left = (wedding.wedding_date - today).days

    return render(request, 'weddings/wedding_page.html', {
        'wedding': wedding,
        'guestbooks': guestbooks,
        'days_left': days_left,
        'galleries': wedding.get_galleries(),
    })

def write_guestbook(request, wedding_id):
    wedding = get_object_or_404(Wedding, pk=wedding_id)

    if request.method == 'POST':
        guest_name = request.POST.get('guest_name')
        message = request.POST.get('message')

        if guest_name and message:
            Guestbook.objects.create(
                wedding=wedding,
                guest_name=guest_name,
                message=message
            )
    return redirect('wedding_page', share_code=wedding.share_code)

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