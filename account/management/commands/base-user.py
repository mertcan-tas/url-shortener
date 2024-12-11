from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Creates a user with predefined data'
    
    def handle(self, *args, **kwargs):
        UserModel = get_user_model()
        name = "Kara Gül"
        email = "kara.gul@outlook.com"
        password = "naga_9192"
        
        if not UserModel.objects.filter(email=email).exists():
            user = UserModel.objects.create_superuser(name=name, email=email, password=password)
            user.is_active = True
            user.is_staff = True
            user.is_advertiser = False
            user.save()
        else:
            pass