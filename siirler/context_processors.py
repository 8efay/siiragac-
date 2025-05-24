from .models import Kategori

def kategoriler(request):
    """
    Context processor that provides all categories to all templates.
    """
    return {
        'kategoriler': Kategori.objects.all()
    } 