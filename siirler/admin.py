from django.contrib import admin
from .models import Siir, Kategori

@admin.register(Kategori)
class KategoriAdmin(admin.ModelAdmin):
    list_display = ('isim',)
    search_fields = ('isim',)

@admin.register(Siir)
class SiirAdmin(admin.ModelAdmin):
    list_display = ('baslik', 'yazar', 'kategori', 'olusturma_tarihi')
    list_filter = ('kategori', 'olusturma_tarihi')
    search_fields = ('baslik', 'icerik', 'yazar__username')
    date_hierarchy = 'olusturma_tarihi'
