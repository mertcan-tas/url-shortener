from django.core.management.base import BaseCommand

from account.models import User

class Command(BaseCommand):
    help = 'Creates a superuser with predefined data'
    
    def handle(self, *args, **kwargs):
        UserModel = User
        name = "Administrator"
        email = "admin123@outlook.com"
        password = "admin123"
        
        if not UserModel.objects.filter(email=email).exists():
            user = UserModel.objects.create_superuser(name=name, email=email, password=password)
            user.is_active = True
            user.is_staff = True
            user.is_advertiser = False
            
            user.save()
            #self.stdout.write(self.style.SUCCESS('[+] Superuser created successfully!'))
        else:
            #self.stdout.write(self.style.WARNING('[-] Superuser already exists!'))
            pass