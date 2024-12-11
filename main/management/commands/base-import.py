from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = "Runs multiple custom management commands"

    def handle(self, *args, **kwargs):
        commands = [            
            "base-admin",
        ]
        
        self.stdout.write()
        self.stdout.write(self.style.WARNING("=========== Commands Start ==========="))
        for command_name in commands:
            try:
                self.stdout.write(self.style.SUCCESS(f"[i] Running Command: {command_name}"))
                call_command(command_name)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"[+] Failed Command: {str(e)}"))
        self.stdout.write(self.style.WARNING("============ Commands End ============"))