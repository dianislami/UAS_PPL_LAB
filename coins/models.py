import json
from django.db import models

class Coin(models.Model):
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=10)
    price = models.FloatField()
    change_24h = models.FloatField()
    market_cap = models.CharField(max_length=50)
    volume_24h = models.CharField(max_length=50)
    circulating_supply = models.CharField(max_length=50)
    max_supply = models.CharField(max_length=50, default='Unlimited')
    rank = models.IntegerField(default=1)
    description = models.TextField()
    sparkline_data = models.CharField(max_length=500, default='[]') 

    def __str__(self):
        return f"{self.name} ({self.symbol})"

    @property
    def sparkline_list(self):
        try:
            return json.loads(self.sparkline_data)
        except Exception:
            # daftar yang menunjukkan beberapa tren
            return [self.price * 0.95, self.price * 0.97, self.price * 0.94, self.price * 1.01, self.price]

class Article(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50)
    time_ago = models.CharField(max_length=50) 
    image_alt = models.CharField(max_length=100, default='Crypto graphic')
    content = models.TextField()

    def __str__(self):
        return self.title
