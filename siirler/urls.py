from django.urls import path
from . import views

urlpatterns = [
    path('', views.anasayfa, name='anasayfa'),
    path('kategori/<int:kategori_id>/', views.kategori_detay, name='kategori_detay'),
    path('siir/<int:siir_id>/', views.siir_detay, name='siir_detay'),
    path('siir/ekle/', views.siir_ekle, name='siir_ekle'),
    path('siir/<int:siir_id>/duzenle/', views.siir_duzenle, name='siir_duzenle'),
    path('siir/<int:siir_id>/sil/onay/', views.siir_sil_onay, name='siir_sil_onay'),
    path('siir/<int:siir_id>/sil/', views.siir_sil, name='siir_sil'),
    path('search/', views.search_results, name='search_results'),
    path('my_poems/', views.my_poems, name='my_poems'),
    path('profile/', views.user_profile, name='my_profile'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('siir/<int:siir_id>/like/', views.like_siir, name='like_siir'),
    path('siir/<int:siir_id>/save/', views.save_siir, name='save_siir'),
    path('draft_poems/', views.draft_poems, name='draft_poems'),
    path('liked_poems/', views.liked_poems, name='liked_poems'),
    path('saved_poems/', views.saved_poems, name='saved_poems'),
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/count/', views.get_unread_notifications_count, name='notifications_count'),
] 