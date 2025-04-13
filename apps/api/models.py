# api/models.py

from django.db import models
from django.contrib.auth import get_user_model
import random
import string

User = get_user_model()

class ShortURL(models.Model):
    original_url = models.URLField(max_length=2000)
    short_code = models.CharField(max_length=10, unique=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")
    
    visits = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='short_urls')
    
    def save(self, *args, **kwargs):
        if not self.short_code:
            self.short_code = self.generate_short_code()
        super().save(*args, **kwargs)
    
    def generate_short_code(self):
        characters = string.ascii_letters + string.digits
        short_code = ''.join(random.choice(characters) for _ in range(6))
        
        # Eğer bu kod zaten varsa, yeni bir kod oluştur
        while ShortURL.objects.filter(short_code=short_code).exists():
            short_code = ''.join(random.choice(characters) for _ in range(6))
        
        return short_code
    
    def __str__(self):
        user_info = f" (by {self.user.username})" if self.user else ""
        return f"{self.original_url} -> {self.short_code}{user_info}"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Kısa URL"
        verbose_name_plural = "Kısa URL'ler"