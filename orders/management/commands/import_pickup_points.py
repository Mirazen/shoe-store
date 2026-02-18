import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from orders.models import PickupPoint


class Command(BaseCommand):
    help = "Импорт пунктов выдачи из CSV файла"

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=str,
            default="data/Пункты выдачи_import.csv",
            help="Путь к CSV файлу",
        )

    def handle(self, *args, **options):
        file_path = options["file"]

        if not file_path.startswith("/"):
            file_path = os.path.join(settings.BASE_DIR, file_path)

        with open(file_path, "r", encoding="utf-8-sig") as f:
            reader = csv.reader(f)

            created_count = 0

            for row in reader:
                if not row or not row[0].strip():
                    continue

                address = row[0].strip()

                _, created = PickupPoint.objects.get_or_create(address=address)

                if created:
                    created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Импорт завершен! Создано пунктов выдачи: {created_count}"
            )
        )
