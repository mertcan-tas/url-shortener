import os
import shutil
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Belirtilen klasör adlarını içeren klasörleri ve db.sqlite3 dosyasını siler'
 
    def handle(self, *args, **options):
        target_directory = getattr(settings, 'BASE_DIR', '.')  # Django proje dizini
        
        folder_names_to_remove = ["__pycache__", "migrations"]
        env_folder = "env"

        folders_deleted = False
        for root, dirs, files in os.walk(target_directory):
            if env_folder in dirs:
                dirs.remove(env_folder)  # env klasörünü es geç
            for folder in dirs:
                if folder in folder_names_to_remove:
                    folder_path = os.path.join(root, folder)
                    self.remove_folder(folder_path)
                    folders_deleted = True

        # db.sqlite3 dosyasını silme işlemi
        if folders_deleted:
            self.remove_database(target_directory)
        else:
            self.stdout.write(self.style.WARNING('[!] Silinecek klasör bulunamadı.'))

    def remove_folder(self, folder_path):
        try:
            shutil.rmtree(folder_path)
            self.stdout.write(self.style.SUCCESS(f'[+] Klasör başarıyla silindi: {folder_path}'))
        except OSError as e:
            self.stdout.write(self.style.ERROR(f'[!] Hata: {e}'))

    def remove_database(self, target_directory):
        db_path = os.path.join(target_directory, 'db.sqlite3')
        if os.path.exists(db_path):
            try:
                os.remove(db_path)
                self.stdout.write(self.style.SUCCESS('[+] db.sqlite3 dosyası başarıyla silindi'))
            except OSError as e:
                self.stdout.write(self.style.ERROR(f'Hata: {e}'))
        else:
            self.stdout.write(self.style.WARNING('[!] db.sqlite3 dosyası bulunamadığı için silinemedi.'))

