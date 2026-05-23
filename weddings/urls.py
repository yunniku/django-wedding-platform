# weddings/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('create/', views.create_wedding, name='create_wedding'),
    path('edit/<int:pk>/', views.edit_wedding, name='edit_wedding'),
    path('delete/<int:pk>/', views.delete_wedding, name='delete_wedding'),
    path('w/<str:share_code>/', views.wedding_page, name='wedding_page'),
    path('guestbook/<int:wedding_id>/', views.write_guestbook, name='write_guestbook'),
]