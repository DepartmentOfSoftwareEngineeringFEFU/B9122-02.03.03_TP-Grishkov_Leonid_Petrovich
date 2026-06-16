import os
import glob
import shutil
from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Полный сброс базы и миграций, создание заново, заполнение seed'

    def handle(self, *args, **options):
        self.stdout.write('=== Запуск полной очистки базы данных и миграций ===\n')

        # 1. Удаление файла базы данных SQLite
        db_file = 'db.sqlite3'
        if os.path.exists(db_file):
            os.remove(db_file)
            self.stdout.write(self.style.SUCCESS(f'Файл базы данных удалён'))
        else:
            self.stdout.write('  База данных не найдена (уже пуста)')

        # 2. Удаление файлов миграций (кроме __init__.py)
        deleted_count = 0
        for file_path in glob.glob('*/migrations/0*.py'):
            os.remove(file_path)
            deleted_count += 1

        # Очистка __pycache__ в migrations
        for cache_path in glob.glob('*/migrations/__pycache__'):
            shutil.rmtree(cache_path)

        self.stdout.write(f'  Удалено файлов миграций: {deleted_count}\n')

        # 3. Очистка папки media
        media_path = 'media'
        if os.path.exists(media_path):
            shutil.rmtree(media_path)
        os.makedirs(media_path)
        self.stdout.write('  Папка media очищена\n')

        # 4. Создание и применение миграций
        self.stdout.write('=== Создание новых миграций ===')
        call_command('makemigrations')

        self.stdout.write('\n=== Применение миграций ===')
        call_command('migrate')

        self.stdout.write('\n=== Заполнение базы ===')
        call_command('seed_data')

        self.stdout.write(self.style.SUCCESS('\nБаза пересоздана и заполнена!'))