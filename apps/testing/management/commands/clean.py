import os
import shutil
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connection
from django.utils import termcolors

class Command(BaseCommand):
    help = 'Project cleanup and database reset'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--noinput', '--no-input',
            action='store_false',
            dest='interactive',
            help='Run without confirmation',
        )

    def handle(self, *args, **options):
        success_style = termcolors.make_style(fg="green")
        error_style = termcolors.make_style(fg="red")
        running_style = termcolors.make_style(fg="blue", opts=("bold",))

        # 1. File and folder cleanup
        self.stdout.write(running_style("\n→ Cleaning up project..."))
        deleted_items = self.clean_project_files()
        
        if deleted_items["pycache"]:
            self.stdout.write(success_style(f"✔ Deleted pycache ({deleted_items['pycache']} items)"))
        if deleted_items["migrations"]:
            self.stdout.write(success_style(f"✔ Deleted migrations ({deleted_items['migrations']} items)"))

        # 2. Database cleanup
        self.stdout.write(running_style("\n→ Cleaning up databases..."))
        self.clean_databases(options['interactive'])

    def clean_project_files(self):
        target_dir = getattr(settings, 'BASE_DIR', '.')
        counters = {"pycache": 0, "migrations": 0}

        for root, dirs, _ in os.walk(target_dir):
            if 'env' in dirs:
                dirs.remove('env')
                
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                if dir_name == "__pycache__":
                    shutil.rmtree(dir_path, ignore_errors=True)
                    counters["pycache"] += 1
                elif dir_name == "migrations":
                    shutil.rmtree(dir_path, ignore_errors=True)
                    counters["migrations"] += 1

        return counters
    
    def clean_databases(self, interactive):
        # SQLite cleanup
        db_path = os.path.join(settings.BASE_DIR, 'db.sqlite3')
        if os.path.exists(db_path):
            os.remove(db_path)
            self.stdout.write(termcolors.make_style(fg="green")(f"✔ SQLite database deleted"))

        # PostgreSQL cleanup
        if interactive:
            confirm = input('\nAll PostgreSQL tables will be deleted! Do you confirm? [y/N]: ')
            if confirm.lower() != 'y':
                return

        with connection.cursor() as cursor:
            try:
                cursor.execute("DROP SCHEMA public CASCADE; CREATE SCHEMA public;")
                self.stdout.write(termcolors.make_style(fg="green")(f"✔ All PostgreSQL tables deleted"))
            except Exception as e:
                self.stdout.write(termcolors.make_style(fg="red")(f"✘ {str(e)}"))
                sys.exit(1)