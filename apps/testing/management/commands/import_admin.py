from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import termcolors
from decouple import config

class Command(BaseCommand):
    help = 'Creates a superuser with predefined data'
    
    def handle(self, *args, **kwargs):
        UserModel = get_user_model()
        name = config('DJANGO_ADMIN_NAME', default='John')
        surname = config('DJANGO_ADMIN_SURNAME', default='Doe')
        email = config('DJANGO_ADMIN_USER_MAIL', default='admin@admin.com')
        password = config('DJANGO_ADMIN_USER_PASWORD', default='admin')
        
        try: 
            if not UserModel.objects.filter(email=email).exists():
                user = UserModel.objects.create_superuser(name=name, surname=surname, email=email,  password=password)
                user.is_active = True
                user.is_staff = True
                user.save()
                
                self.stdout.write(termcolors.make_style(fg="green")('✔ Superuser created successfully!'))
            else:
                self.stdout.write(termcolors.make_style(fg="red")(f"✘ Superuser already exists!"))
                sys.exit(1)
                
        except Exception as e:
            self.stdout.write(termcolors.make_style(fg="red")(f"✘ {str(e)}"))
            sys.exit(1)