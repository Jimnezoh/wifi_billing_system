#model to store wifi access code and track payment.

from django.utils import timezone
from datetime import timedelta
from django.db import models
import random
import string
from users.models import User

# Create your models here.

class WifiAccessCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, unique=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    duration_minutes = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def has_expired(self):
        return self.expires_at <= timezone.now()
    
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_code()
        if not self.expires_at and self.duration_minutes is not None:
            self.expires_at = timezone.now() + timedelta(minutes=self.duration_minutes)
        super().save(*args, **kwargs)

    @staticmethod
    def generate_code(length=6):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

    def __str__(self):
        return f"{self.code} for {self.user.phone_number}"