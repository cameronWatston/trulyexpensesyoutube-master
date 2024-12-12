from django.db import models
from django.contrib.auth.models import User

class MonthlyFinance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    savings_goal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    debt = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Monthly Finance"
