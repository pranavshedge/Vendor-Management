from django.db import models
from django.db import models
from django.utils import timezone
import secrets

class CustomToken(models.Model):
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    @classmethod
    def generate_token(cls):
        return secrets.token_hex(20)  # Generates a random hex token of length 20

    @classmethod
    def create_token(cls):
        token = cls.generate_token()
        return cls.objects.create(token=token)
    
    class Meta:
        app_label = 'authentication'  # Replace 'your_app_name' with the actual name of your Django app

    def __str__(self):
        return self.token
