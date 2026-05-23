# weddings/admin.py
from django.contrib import admin
from .models import Wedding, Guestbook

@admin.register(Wedding)
class WeddingAdmin(admin.ModelAdmin):
    list_display = ['groom_name', 'bride_name', 'wedding_date', 'theme', 'share_code', 'user']
    list_filter = ['theme', 'wedding_date']
    search_fields = ['groom_name', 'bride_name', 'user__email']
    readonly_fields = ['share_code', 'created_at', 'updated_at']

@admin.register(Guestbook)
class GuestbookAdmin(admin.ModelAdmin):
    list_display = ['guest_name', 'wedding', 'created_at']
    search_fields = ['guest_name', 'wedding__groom_name']