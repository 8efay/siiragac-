from django import forms
from .models import Siir, UserProfile

class SiirForm(forms.ModelForm):
    class Meta:
        model = Siir
        fields = ['baslik', 'icerik', 'kategori', 'muzik_dosyasi', 'status']
        widgets = {
            'icerik': forms.Textarea(attrs={'rows': 10}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar', 'bio']

# class YorumForm(forms.ModelForm):
#     class Meta:
#         model = Yorum
#         fields = ['icerik']
#         widgets = {
#             'icerik': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Yorumunuzu yazın...'}),
#         } 