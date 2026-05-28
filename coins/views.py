from django.shortcuts import render, get_object_or_404
from .models import Coin, Article

def explore_coins(request):
    # Ambil semua koin dari database SQLite diurutkan berdasarkan peringkat
    all_coins = Coin.objects.all().order_by('rank')
    return render(request, 'coins/explore.html', {'coins': all_coins})

def coin_detail(request, pk):
    # Cari koin aktif berdasarkan kunci primer
    coin = get_object_or_404(Coin, pk=pk)
    # Ambil artikel mengenai analisis blockchain atau teknologi
    articles = Article.objects.all()[:3]
    return render(request, 'coins/detail.html', {
        'coin': coin,
        'articles': articles
    })
