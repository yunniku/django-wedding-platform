# weddings/forms.py
from django import forms
from .models import Wedding, Guestbook


class WeddingForm(forms.ModelForm):
    class Meta:
        model = Wedding
        fields = [
            'groom_name', 'bride_name', 'wedding_date',
            'venue', 'venue2', 'message',
            'groom_phone', 'bride_phone',
            'groom_account', 'bride_account',
            'map_url', 'theme', 'photo', 'photo_orientation',
            'gallery1', 'gallery2', 'gallery3', 'gallery4',
            'gallery5', 'gallery6', 'gallery7', 'gallery8',
        ]
        widgets = {
            'wedding_date': forms.DateInput(attrs={'type': 'date'}),
            'message': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_wedding_date(self):
        from datetime import date
        wedding_date = self.cleaned_data.get('wedding_date')
        if wedding_date and wedding_date < date.today():
            raise forms.ValidationError('결혼식 날짜는 오늘 이후여야 해요!')
        return wedding_date


class GuestbookForm(forms.ModelForm):
    class Meta:
        model = Guestbook
        fields = ['guest_name', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3}),
        }