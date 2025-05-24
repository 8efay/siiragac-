from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

class Kategori(models.Model):
    isim = models.CharField(max_length=100)
    display_name = models.CharField(max_length=100, default='')
    aciklama = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.display_name
    
    class Meta:
        verbose_name_plural = "Kategoriler"

class Siir(models.Model):
    STATUS_CHOICES = [
        ('draft', _('Taslak')),
        ('published', _('Yayınlandı')),
    ]

    baslik = models.CharField(max_length=200)
    icerik = models.TextField()
    yazar = models.ForeignKey(User, on_delete=models.CASCADE)
    kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE)
    olusturma_tarihi = models.DateTimeField(auto_now_add=True)
    muzik_dosyasi = models.FileField(upload_to='muzikler/', null=True, blank=True)
    likes = models.ManyToManyField(User, related_name='liked_siirler', blank=True)
    saved_by = models.ManyToManyField(User, related_name='saved_siirler', blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    
    def __str__(self):
        return self.baslik
    
    class Meta:
        verbose_name_plural = "Şiirler"
        ordering = ('-olusturma_tarihi',)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    followers = models.ManyToManyField(User, related_name='following', blank=True)

    def __str__(self):
        return self.user.username

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('like', 'Beğeni'),
        ('follow', 'Takip'),
        ('save', 'Kaydetme'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications')
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    siir = models.ForeignKey(Siir, on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Bildirimler"

    def __str__(self):
        if self.notification_type == 'like':
            return f"{self.sender.username} şiirinizi beğendi"
        elif self.notification_type == 'follow':
            return f"{self.sender.username} sizi takip etmeye başladı"
        elif self.notification_type == 'save':
            return f"{self.sender.username} şiirinizi kaydetti"

# Kullanıcı oluşturulduğunda otomatik olarak profil oluşturma
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

# Kullanıcı kaydedildiğinde profili kaydetme
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()

# Bildirim sinyalleri
@receiver(post_save, sender=Siir)
def create_like_or_save_notification(sender, instance, created, **kwargs):
    if not created:
        # Check for likes
        previous_likes = Siir.objects.get(pk=instance.pk).likes.all()
        current_likes = instance.likes.all()
        new_likes = set(current_likes) - set(previous_likes)
        for user in new_likes:
             if user != instance.yazar:
                 Notification.objects.create(
                     user=instance.yazar,
                     sender=user,
                     notification_type='like',
                     siir=instance
                 )
                 
        # Check for saves
        previous_saves = Siir.objects.get(pk=instance.pk).saved_by.all()
        current_saves = instance.saved_by.all()
        new_saves = set(current_saves) - set(previous_saves)
        for user in new_saves:
             if user != instance.yazar:
                  Notification.objects.create(
                      user=instance.yazar,
                      sender=user,
                      notification_type='save',
                      siir=instance
                  )

@receiver(post_save, sender=UserProfile)
def create_follow_notification(sender, instance, created, **kwargs):
    if not created and instance.followers.exists():
        for follower in instance.followers.all():
            Notification.objects.create(
                user=instance.user,
                sender=follower,
                notification_type='follow'
            )
