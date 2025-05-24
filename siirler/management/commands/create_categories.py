from django.core.management.base import BaseCommand
from siirler.models import Kategori

class Command(BaseCommand):
    help = 'Şiir kategorilerini oluşturur'

    def handle(self, *args, **kwargs):
        categories = [
            {
                'isim': 'Lirik Şiir',
                'display_name': '💖 Duygusal Şiirler',
                'aciklama': 'Aşk, özlem, sevinç, hüzün gibi duyguları işler.'
            },
            {
                'isim': 'Epik Şiir',
                'display_name': '⚔️ Kahramanlık Şiirleri',
                'aciklama': 'Savaşlar, yiğitlikler, kahramanlık hikâyeleri içerir.'
            },
            {
                'isim': 'Pastoral Şiir',
                'display_name': '🌿 Doğa Şiirleri',
                'aciklama': 'Kır yaşamı, doğa sevgisi ve huzur temasını işler.'
            },
            {
                'isim': 'Didaktik Şiir',
                'display_name': '📚 Öğretici Şiirler',
                'aciklama': 'Bilgi verme, öğüt verme veya ders verme amacı taşır.'
            },
            {
                'isim': 'Satirik Şiir',
                'display_name': '😏 Eleştirel / Mizahi Şiirler',
                'aciklama': 'Toplumu, kişileri veya olayları hicivle eleştirir.'
            }
        ]

        for category in categories:
            Kategori.objects.get_or_create(
                isim=category['isim'],
                defaults={
                    'display_name': category['display_name'],
                    'aciklama': category['aciklama']
                }
            )
            self.stdout.write(
                self.style.SUCCESS(f'Kategori oluşturuldu: {category["display_name"]}')
            ) 