from django.db import models
from products.models import Product
from accounts.models import CustomUser


class Order(models.Model):
    STATUS_UNITS = [
        ("new", "Новый"),
        ("complete", "Завершен"),
        ("cancelled", "Отменен"),
    ]
    order_number = models.SmallIntegerField(unique=True, verbose_name="Номер заказа")
    order_date = models.DateField(verbose_name="Дата заказа")
    delivery_date = models.DateField(verbose_name="Дата доставки")
    pickup_point = models.ForeignKey(
        "PickupPoint", on_delete=models.CASCADE, verbose_name="Адрес пункта выдачи"
    )
    customer = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, verbose_name="ФИО пользователя"
    )
    pickup_code = models.IntegerField(verbose_name="Код получения")
    status = models.CharField(
        max_length=40, choices=STATUS_UNITS, verbose_name="Статус заказа"
    )

    def __str__(self):
        return f"Заказ №{self.order_number}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class OrderItem(models.Model):
    order = models.ForeignKey("Order", on_delete=models.CASCADE, verbose_name="Заказ")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.SmallIntegerField(default=1, verbose_name="Количество")

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"

    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказа"


class PickupPoint(models.Model):
    address = models.CharField(max_length=200, verbose_name="Адрес")

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = "Пункт выдачи"
        verbose_name_plural = "Пункты выдачи"
