from django.db import models
from shortuuid.django_fields import ShortUUIDField
from account.models import User

class ShortenedLink(models.Model):
    id = ShortUUIDField(length=16,max_length=40,alphabet="abcdefg1234",primary_key=True,editable=False)
    url = models.URLField()
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")
    expires_at = models.DateTimeField(null=True, blank=True)
    click_count = models.PositiveIntegerField(default=0)

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="user")
    
    def __str__(self):
        return self.url

    def increment_click_count(self):
        self.click_count += 1
        self.save()

    class Meta:
        verbose_name = "Shortened Link"
        verbose_name_plural = "Shortened Links"