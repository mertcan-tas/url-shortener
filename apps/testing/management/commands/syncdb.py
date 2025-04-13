from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connections, transaction
from django.utils import termcolors

class Command(BaseCommand):
    help = "Automatically runs makemigrations for all apps in PROJECT_APPS"

    def handle(self, *args, **kwargs):
        # Settings'den app listesini al
        project_apps = getattr(settings, "PROJECT_APPS", [])
        
        if not project_apps:
            self.stdout.write(self.style.ERROR("PROJECT_APPS not found in settings!"))
            return
        
        # Her app için makemigrations komutu oluştur
        commands = [f"makemigrations {app}" for app in project_apps]
 
        for command_name in commands:
            try:
                # Her komut için yeni bağlantı
                with connections['default'].cursor() as cursor:
                    self.stdout.write(termcolors.make_style(fg="green")(f"Running: {command_name}"))
                    cursor.execute("SET statement_timeout = 0;")
                
                # Komutu çalıştır
                call_command(*command_name.split())
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed: {str(e)}"))
                connections['default'].needs_rollback = False
                transaction.rollback(using='default')
                break