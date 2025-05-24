from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from siirler.models import UserProfile

User = get_user_model()

class Command(BaseCommand):
    help = 'Eksik kullanıcı profillerini oluşturur'

    def handle(self, *args, **kwargs):
        users_without_profile = User.objects.filter(userprofile__isnull=True)
        count = 0
        for user in users_without_profile:
            UserProfile.objects.create(user=user)
            self.stdout.write(self.style.SUCCESS(f'Profil oluşturuldu: {user.username}'))
            count += 1
        
        if count > 0:
            self.stdout.write(self.style.SUCCESS(f'{count} adet eksik kullanıcı profili oluşturuldu.'))
        else:
            self.stdout.write(self.style.SUCCESS('Eksik kullanıcı profili bulunmamaktadır.')) 