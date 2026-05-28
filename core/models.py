from django.db import models
from django.contrib.auth.models import User

class Coin(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=15, unique=True)
    rank = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=20, decimal_places=4, default=0.00)
    change_24h = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    market_cap = models.CharField(max_length=50, blank=True)
    volume_24h = models.CharField(max_length=50, blank=True)
    circulating_supply = models.CharField(max_length=50, blank=True)
    max_supply = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['rank']

    def __str__(self):
        return f"{self.name} ({self.symbol})"


class Article(models.Model):
    CATEGORY_CHOICES = [
        ('ANALYSIS', 'Market Analysis'),
        ('REGULATION', 'Regulation'),
        ('TECH', 'Technology'),
    ]
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='ANALYSIS')
    content = models.TextField()
    image_alt = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='portfolios')
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=8, default=0.00)
    avg_buy_price = models.DecimalField(max_digits=20, decimal_places=4, default=0.00)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'coin')

    def __str__(self):
        return f"{self.user.username}'s {self.coin.symbol} position"

    @property
    def current_value(self):
        return self.amount * self.coin.price

    @property
    def total_cost(self):
        return self.amount * self.avg_buy_price

    @property
    def profit_loss(self):
        return self.current_value - self.total_cost

    @property
    def profit_percentage(self):
        cost = self.total_cost
        if cost == 0:
            return 0
        return (self.profit_loss / cost) * 100
