import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from accounts.models import CustomUser


class Command(BaseCommand):
    help = "Импорт пользователей из CSV файла"

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=str,
            default="data/user_import.csv",
            help="Путь к CSV файлу",
        )

    def handle(self, *args, **options):
        file_path = options["file"]

        if not file_path.startswith("/"):
            file_path = os.path.join(settings.BASE_DIR, file_path)

        # Соответствие ролей из CSV и модели
        ROLE_MAP = {
            "Администратор": "admin",
            "Менеджер": "manager",
            "Авторизированный клиент": "client",
        }

        with open(file_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f, delimiter=";")

            created_count = 0
            updated_count = 0

            for row in reader:
                # Пропускаем пустые строки
                if not row["Логин"] or not row["Пароль"]:
                    continue

                email = row["Логин"].strip()
                full_name = row["ФИО"].strip()
                password = row["Пароль"].strip()
                role_raw = row["Роль сотрудника"].strip()

                # Получаем роль из маппинга
                role = ROLE_MAP.get(role_raw, "client")

                # Получаем или создаём пользователя
                user, created = CustomUser.objects.update_or_create(
                    email=email,
                    defaults={
                        "full_name": full_name,
                        "role": role,
                    },
                )

                # Устанавливаем пароль (только при создании, чтобы не сбрасывать существующий)
                if created:
                    user.set_password(password)
                    user.save()
                    created_count += 1
                else:
                    updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Импорт завершен! Создано: {created_count}, Обновлено: {updated_count}"
            )
        )
