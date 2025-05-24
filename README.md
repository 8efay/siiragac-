# Şiir Ağacı

Şiir Ağacı, şiir severlerin şiirlerini paylaşabilecekleri, birbirlerini takip edebilecekleri ve etkileşimde bulunabilecekleri bir sosyal medya platformudur.

## Özellikler

- Şiir paylaşma ve düzenleme
- Kullanıcı profilleri ve takip sistemi
- Şiir beğenme ve kaydetme
- Bildirim sistemi
- Kategori bazlı şiir organizasyonu
- Müzik dosyası ekleme desteği

## Kurulum

1. Projeyi klonlayın:
```bash
git clone https://github.com/8efay/siiragac-.git
cd siiragac-
```

2. Sanal ortam oluşturun ve aktifleştirin:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac için
venv\Scripts\activate     # Windows için
```

3. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

4. Veritabanı migrasyonlarını uygulayın:
```bash
python manage.py migrate
```

5. Geliştirme sunucusunu başlatın:
```bash
python manage.py runserver
```

## Teknolojiler

- Django 5.0.2
- Python 3.11.5
- SQLite
- Bootstrap 5
- Django AllAuth
- Crispy Forms

## Katkıda Bulunma

1. Bu depoyu fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Bir Pull Request oluşturun

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın. 