from django.contrib import admin
from .models import Siir, Kategori, UserProfile, Notification

@admin.register(Kategori)
class KategoriAdmin(admin.ModelAdmin):
    list_display = ('isim', 'display_name')
    search_fields = ('isim', 'display_name')

@admin.register(Siir)
class SiirAdmin(admin.ModelAdmin):
    list_display = ('baslik', 'yazar', 'kategori', 'olusturma_tarihi', 'status')
    list_filter = ('kategori', 'olusturma_tarihi', 'status')
    search_fields = ('baslik', 'icerik', 'yazar__username')
    date_hierarchy = 'olusturma_tarihi'

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')
    search_fields = ('user__username', 'bio')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'sender', 'notification_type', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('user__username', 'sender__username')
