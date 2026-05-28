from django.contrib import admin
from .models import Coin, Article

@admin.register(Coin)
class CoinAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol', 'price', 'change_24h', 'rank')
    search_fields = ('name', 'symbol')
    list_filter = ('rank', 'change_24h')

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'time_ago')
    search_fields = ('title', 'category')
