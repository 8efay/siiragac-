from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from .models import Siir, Kategori, UserProfile
from .forms import SiirForm, UserProfileForm

User = get_user_model()

import random

def anasayfa(request):
    all_siirler = list(Siir.objects.all())
    random_siirler = random.sample(all_siirler, min(len(all_siirler), 5)) # En fazla 5 rastgele şiir
    return render(request, 'siirler/anasayfa.html', {
        'siirler': random_siirler,
    })

def kategori_detay(request, kategori_id):
    kategori = get_object_or_404(Kategori, id=kategori_id)
    siirler = Siir.objects.filter(kategori=kategori).order_by('-olusturma_tarihi')
    return render(request, 'siirler/kategori_detay.html', {
        'kategori': kategori,
        'siirler': siirler
    })

def siir_detay(request, siir_id):
    siir = get_object_or_404(Siir, id=siir_id)
    return render(request, 'siirler/siir_detay.html', {'siir': siir})

@login_required
def siir_ekle(request):
    if request.method == 'POST':
        form = SiirForm(request.POST, request.FILES)
        if form.is_valid():
            siir = form.save(commit=False)
            siir.yazar = request.user
            siir.save()
            messages.success(request, 'Şiir başarıyla eklendi!')
            return redirect('my_poems') # Şiir ekledikten sonra kendi şiirlerine yönlendir
    else:
        form = SiirForm()
    return render(request, 'siirler/siir_ekle.html', {'form': form})

@login_required
def siir_duzenle(request, siir_id):
    siir = get_object_or_404(Siir, id=siir_id, yazar=request.user)
    if request.method == 'POST':
        form = SiirForm(request.POST, request.FILES, instance=siir)
        if form.is_valid():
            form.save()
            messages.success(request, 'Şiir başarıyla güncellendi!')
            return redirect('my_poems') # Şiir düzenledikten sonra kendi şiirlerine yönlendir
    else:
        form = SiirForm(instance=siir)
    return render(request, 'siirler/siir_duzenle.html', {'form': form})

@login_required
def siir_sil_onay(request, siir_id):
    siir = get_object_or_404(Siir, id=siir_id, yazar=request.user)
    return render(request, 'siirler/siir_sil_onay.html', {'siir': siir})

@login_required
def siir_sil(request, siir_id):
    siir = get_object_or_404(Siir, id=siir_id, yazar=request.user)
    if request.method == 'POST':
        siir.delete()
        messages.success(request, 'Şiir başarıyla silindi!')
        return redirect('my_poems') # Şiir sildikten sonra kendi şiirlerine yönlendir
    return redirect('siir_sil_onay', siir_id=siir_id)

def search_results(request):
    query = request.GET.get('q')
    siirler = Siir.objects.all()
    if query:
        siirler = siirler.filter(
            Q(baslik__icontains=query) |
            Q(yazar__username__icontains=query)
        ).distinct()
    return render(request, 'siirler/search_results.html', {'query': query, 'siirler': siirler})

@login_required
def my_poems(request):
    siirler = Siir.objects.filter(yazar=request.user).order_by('-olusturma_tarihi')
    return render(request, 'siirler/my_poems.html', {'siirler': siirler})

@login_required
def user_profile(request, username=None):
    if username:
        user = get_object_or_404(User, username=username)
        is_own_profile = False
    else:
        user = request.user
        is_own_profile = True

    profile = user.userprofile
    siirler = Siir.objects.filter(yazar=user).order_by('-olusturma_tarihi')

    # İstatistikleri hesaplama
    total_poems = siirler.count()
    published_poems = siirler.filter(status='published').count()
    draft_poems_count = siirler.filter(status='draft').count()
    total_likes_received = sum(siir.likes.count() for siir in siirler)
    # Kullanıcının kaydettiği şiir sayısı
    total_liked_poems = user.saved_siirler.count() if request.user.is_authenticated else 0

    if request.method == 'POST' and is_own_profile:
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil başarıyla güncellendi!')
            return redirect('my_profile')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'siirler/user_profile.html', {
        'user_obj': user,
        'profile': profile,
        'siirler': siirler,
        'form': form,
        'is_own_profile': is_own_profile,
        'total_poems': total_poems,
        'published_poems': published_poems,
        'draft_poems_count': draft_poems_count,
        'total_likes_received': total_likes_received,
        'total_saved_poems': total_liked_poems,
    })

@login_required
def like_siir(request, siir_id):
    siir = get_object_or_404(Siir, id=siir_id)
    if request.user in siir.likes.all():
        siir.likes.remove(request.user)
        liked = False
    else:
        siir.likes.add(request.user)
        liked = True

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'liked': liked, 'likes_count': siir.likes.count()})

    return redirect(request.META.get('HTTP_REFERER', 'anasayfa'))

@login_required
def save_siir(request, siir_id):
    siir = get_object_or_404(Siir, id=siir_id)
    if request.user in siir.saved_by.all():
        siir.saved_by.remove(request.user)
        saved = False
    else:
        siir.saved_by.add(request.user)
        saved = True

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'saved': saved, 'saved_count': siir.saved_by.count()})

    return redirect(request.META.get('HTTP_REFERER', 'anasayfa'))

@login_required
def draft_poems(request):
    siirler = Siir.objects.filter(yazar=request.user, status='draft').order_by('-olusturma_tarihi')
    return render(request, 'siirler/draft_poems.html', {'siirler': siirler})

@login_required
def liked_poems(request):
    # Kullanıcının beğendiği şiirler ManyToMany alanı üzerinden erişilebilir
    siirler = request.user.liked_siirler.all().order_by('-olusturma_tarihi')
    return render(request, 'siirler/liked_poems.html', {'siirler': siirler})

@login_required
def saved_poems(request):
    # Kullanıcının kaydettiği şiirler ManyToMany alanı üzerinden erişilebilir
    siirler = request.user.saved_siirler.all().order_by('-olusturma_tarihi')
    return render(request, 'siirler/saved_poems.html', {'siirler': siirler})

@login_required
def notifications(request):
    notifications = request.user.notifications.all()
    unread_count = notifications.filter(is_read=False).count()
    
    # Tüm bildirimleri okundu olarak işaretle
    notifications.update(is_read=True)
    
    return render(request, 'siirler/notifications.html', {
        'notifications': notifications,
        'unread_count': unread_count
    })

@login_required
def get_unread_notifications_count(request):
    count = request.user.notifications.filter(is_read=False).count()
    return JsonResponse({'count': count})

@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    if user_to_follow != request.user:
        request.user.userprofile.followers.add(user_to_follow)
        messages.success(request, f'{user_to_follow.username} kullanıcısını takip etmeye başladınız!')
    return redirect('user_profile', username=username)

@login_required
def unfollow_user(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)
    if user_to_unfollow != request.user:
        request.user.userprofile.followers.remove(user_to_unfollow)
        messages.success(request, f'{user_to_unfollow.username} kullanıcısını takip etmeyi bıraktınız!')
    return redirect('user_profile', username=username)
