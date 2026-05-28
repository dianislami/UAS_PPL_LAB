from django.db import models
from django.contrib.auth.models import User
from coins.models import Coin

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='portfolio_holdings')
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE)
    amount = models.FloatField(default=0.0)
    avg_buy_price = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.user.username}'s {self.coin.symbol} Holding"

    @property
    def total_value(self):
        return self.amount * self.coin.price

    @property
    def holding_cost(self):
        return self.amount * self.avg_buy_price

    @property
    def profit_loss_percentage(self):
        if self.avg_buy_price == 0:
            return 0.0
        return ((self.coin.price - self.avg_buy_price) / self.avg_buy_price) * 100

    @property
    def profit_loss_value(self):
        return self.total_value - self.holding_cost

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('BUY', 'BUY'),
        ('SELL', 'SELL'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    coin_symbol = models.CharField(max_length=15)
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.FloatField()
    price = models.FloatField()
    date_str = models.CharField(max_length=50) # formats like "May 24, 2026"
    status = models.CharField(max_length=20, default='Completed')

    def __str__(self):
        return f"{self.user.username}: {self.type} {self.amount} {self.coin_symbol}"
