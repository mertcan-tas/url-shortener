from django.core.management.base import BaseCommand
from django.core.management import call_command  # Import call_command
from django.db import connections, transaction
from django.utils import termcolors
from time import sleep
from decouple import config


class Command(BaseCommand):
    help = "Safe command runner with transaction handling"
    
    def handle(self, *args, **kwargs):
        commands = [
            "clean --no-input",
            "syncdb",
            "migrate",
            "base_import",
            "flush_redis",
        ]
        
        for command_name in commands:
            try:
                with connections['default'].cursor() as cursor:
                    self.stdout.write("\n")
                    self.stdout.write(termcolors.make_style(fg="yellow", opts=("bold",))(f"→ Running: {command_name}"))
                    cursor.execute("SET statement_timeout = 0;")
                
                call_command(*command_name.split())
            
            except Exception as e:
                self.stdout.write(termcolors.make_style(fg="red")(f"✘ {str(e)}"))
                connections['default'].needs_rollback = False
                transaction.rollback(using='default')
                break
                sys.exit(1)

        self.stdout.write("\n")
        self.stdout.write(termcolors.make_style(fg="cyan")('✔ all command runing complate!'), )
        sleep(config("TESTING_SLEEP_TIMEOUT", cast=int, default=5))