import csv
from django.core.management.base import BaseCommand
from django.conf import settings
from products.models import Product, Provider, Manufacturer, Category
import os


class Command(BaseCommand):
    help = "Импорт товаров из CSV файла"

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=str,
            default="data/Tovar.csv",
            help="Путь к CSV файлу",
        )

    def handle(self, *args, **options):
        file_path = options["file"]

        if not file_path.startswith("/"):
            file_path = os.path.join(settings.BASE_DIR, file_path)

        with open(file_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f, delimiter=";")

            created_count = 0
            updated_count = 0

            for row in reader:
                if not row["Артикул"] or not row["Наименование товара"]:
                    continue

                # Получаем или создаём справочники
                provider, _ = Provider.objects.get_or_create(
                    name=row["Поставщик"].strip()
                )
                manufacturer, _ = Manufacturer.objects.get_or_create(
                    name=row["Производитель"].strip()
                )
                category, _ = Category.objects.get_or_create(
                    name=row["Категория товара"].strip()
                )

                # Очищаем и преобразуем данные
                price = row["Цена"].strip()
                discount = row["Действующая скидка"].strip()
                stock = row["Кол-во на складе"].strip()

                try:
                    price_val = int(price) if price else 0
                except ValueError:
                    price_val = 0

                try:
                    discount_val = int(discount) if discount else 0
                except ValueError:
                    discount_val = 0

                try:
                    stock_val = int(stock) if stock else 0
                except ValueError:
                    stock_val = 0

                # Получаем или создаём товар
                product, created = Product.objects.update_or_create(
                    article=row["Артикул"].strip(),
                    defaults={
                        "name": row["Наименование товара"].strip(),
                        "price": price_val,
                        "provider": provider,
                        "manufacturer": manufacturer,
                        "category": category,
                        "discount": discount_val,
                        "stock_quantity": stock_val,
                        "description": row["Описание товара"].strip(),
                        "image": row["Фото"].strip() if row["Фото"].strip() else None,
                    },
                )

                if created:
                    created_count += 1
                else:
                    updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Импорт завершен! Создано: {created_count}, Обновлено: {updated_count}"
            )
        )
