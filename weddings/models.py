# weddings/models.py
from django.db import models
from django.contrib.auth.models import User
import uuid

class Wedding(models.Model):
    THEME_CHOICES = [
        ('classic', 'Classic'),
        ('modern', 'Modern'),
        ('romantic', 'Romantic'),
    ]
    ORIENTATION_CHOICES = [
        ('landscape', '가로형'),
        ('portrait', '세로형'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='weddings')
    share_code = models.CharField(max_length=12, unique=True, blank=True)

    # 기본 정보
    groom_name = models.CharField(max_length=50)
    bride_name = models.CharField(max_length=50)
    wedding_date = models.DateField()
    venue = models.CharField(max_length=200)
    venue2 = models.CharField(max_length=200, blank=True)
    message = models.TextField(blank=True)

    # 연락처
    groom_phone = models.CharField(max_length=20, blank=True)
    bride_phone = models.CharField(max_length=20, blank=True)

    # 계좌번호
    groom_account = models.CharField(max_length=100, blank=True)
    bride_account = models.CharField(max_length=100, blank=True)

    # 사진
    photo = models.ImageField(upload_to='wedding/cover/', blank=True, null=True)
    photo_orientation = models.CharField(max_length=10, choices=ORIENTATION_CHOICES, default='landscape')

    # 갤러리
    gallery1 = models.ImageField(upload_to='wedding/gallery/', blank=True, null=True)
    gallery2 = models.ImageField(upload_to='wedding/gallery/', blank=True, null=True)
    gallery3 = models.ImageField(upload_to='wedding/gallery/', blank=True, null=True)
    gallery4 = models.ImageField(upload_to='wedding/gallery/', blank=True, null=True)
    gallery5 = models.ImageField(upload_to='wedding/gallery/', blank=True, null=True)
    gallery6 = models.ImageField(upload_to='wedding/gallery/', blank=True, null=True)
    gallery7 = models.ImageField(upload_to='wedding/gallery/', blank=True, null=True)
    gallery8 = models.ImageField(upload_to='wedding/gallery/', blank=True, null=True)

    # 테마
    theme = models.CharField(max_length=10, choices=THEME_CHOICES, default='classic')

    # 지도
    map_url = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # 공유 코드 자동 생성
        if not self.share_code:
            self.share_code = uuid.uuid4().hex[:8].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.groom_name} ♥ {self.bride_name}"

    def get_galleries(self):
        galleries = []
        for i in range(1, 9):
            img = getattr(self, f'gallery{i}')
            if img:
                galleries.append(img.url)
        return galleries

    class Meta:
        ordering = ['-created_at']


class Guestbook(models.Model):
    wedding = models.ForeignKey(Wedding, on_delete=models.CASCADE, related_name='guestbooks')
    guest_name = models.CharField(max_length=50)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.guest_name} → {self.wedding}"

    class Meta:
        ordering = ['-created_at']