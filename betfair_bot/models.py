from django.db import models
from django.contrib.auth.models import User

class Market(models.Model):
    market_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    # Add more fields as necessary

    def __str__(self):
        return self.name

class Bet(models.Model):
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Optional, if tracking users
    selection = models.CharField(max_length=255)
    stake = models.DecimalField(max_digits=6, decimal_places=2)
    odds = models.DecimalField(max_digits=5, decimal_places=2)
    won = models.BooleanField(default=False)
    payout = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.selection} - {'Won' if self.won else 'Lost'}"

    @property
    def calculate_profit(self):
        """Calculate profit for this bet."""
        if self.won:
            return self.payout - self.stake
        return -self.stake

    class Meta:
        ordering = ['-market__start_time']

