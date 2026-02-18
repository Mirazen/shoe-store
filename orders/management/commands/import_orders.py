import csv
import os
from datetime import datetime
from django.core.management.base import BaseCommand
from django.conf import settings
from orders.models import Order, OrderItem, PickupPoint
from accounts.models import CustomUser
from products.models import Product


class Command(BaseCommand):
    help = "Импорт заказов из CSV файла"

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=str,
            default="data/Заказ_import.csv",
            help="Путь к CSV файлу",
        )

    def handle(self, *args, **options):
        file_path = options["file"]

        if not file_path.startswith("/"):
            file_path = os.path.join(settings.BASE_DIR, file_path)

        # Соответствие статусов
        STATUS_MAP = {
            "Новый": "new",
            "Завершен": "complete",
            "Отменен": "cancelled",
        }

        with open(file_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f, delimiter=";")

            created_count = 0
            updated_count = 0

            for row in reader:
                # Пропускаем пустые строки
                if not row["Номер заказа"] or not row["Номер заказа"].strip():
                    continue

                # Номер заказа
                try:
                    order_number = int(row["Номер заказа"].strip())
                except ValueError:
                    continue

                # Дата заказа
                try:
                    order_date = datetime.strptime(
                        row["Дата заказа"].strip(), "%d.%m.%Y"
                    ).date()
                except (ValueError, KeyError) as e:
                    self.stdout.write(
                        f"WARNING: Ошибка даты заказа: {e}, row: {row.get('Номер заказа')}"
                    )
                    order_date = None

                # Дата доставки
                try:
                    delivery_date = datetime.strptime(
                        row["Дата доставки"].strip(), "%d.%m.%Y"
                    ).date()
                except (ValueError, KeyError) as e:
                    self.stdout.write(
                        f"WARNING: Ошибка даты доставки: {e}, row: {row.get('Номер заказа')}"
                    )
                    delivery_date = None

                # Пункт выдачи (по ID)
                try:
                    pickup_point_id = int(row["Адрес пункта выдачи"].strip())
                    pickup_point = PickupPoint.objects.get(id=pickup_point_id)
                except (ValueError, KeyError, PickupPoint.DoesNotExist):
                    pickup_point = None

                # Клиент (по ФИО)
                customer_name = row["ФИО авторизированного клиента"].strip()
                customer = CustomUser.objects.filter(full_name=customer_name).first()

                # Код получения
                try:
                    pickup_code = int(row["Код для получения"].strip())
                except (ValueError, KeyError):
                    pickup_code = 0

                # Статус
                status_raw = row["Статус заказа"].strip()
                status = STATUS_MAP.get(status_raw, "new")

                # Создаём или обновляем заказ
                order, created = Order.objects.update_or_create(
                    order_number=order_number,
                    defaults={
                        "order_date": order_date,
                        "delivery_date": delivery_date,
                        "pickup_point": pickup_point,
                        "customer": customer,
                        "pickup_code": pickup_code,
                        "status": status,
                    },
                )

                if created:
                    created_count += 1
                else:
                    updated_count += 1

                # Парсим товары в заказе: "А112Т4, 2, F635R4, 2"
                articles_str = row.get("Артикул заказа", "").strip()
                if articles_str:
                    # Удаляем старые позиции
                    OrderItem.objects.filter(order=order).delete()

                    # Разбиваем на пары: артикул, количество
                    parts = [p.strip() for p in articles_str.split(",")]
                    for i in range(0, len(parts) - 1, 2):
                        article = parts[i]
                        try:
                            quantity = int(parts[i + 1])
                        except (ValueError, IndexError):
                            quantity = 1

                        # Находим товар по артикулу
                        product = Product.objects.filter(article=article).first()
                        if product:
                            OrderItem.objects.create(
                                order=order,
                                product=product,
                                quantity=quantity,
                            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Импорт завершен! Создано: {created_count}, Обновлено: {updated_count}"
            )
        )
