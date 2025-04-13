from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.utils import termcolors

class Command(BaseCommand):
    help = "Runs multiple custom management commands"
    
    def handle(self, *args, **kwargs):
        commands = [            
            "import_admin",
        ]
        
        for command_name in commands:
            try:
                self.stdout.write(termcolors.make_style(fg="blue", opts=("bold",))(f"→ Running: {command_name}"))
                call_command(command_name)
            except Exception as e:
                self.stdout.write(termcolors.make_style(fg="red")(f"✘ {str(e)}"))
                sys.exit(1)
