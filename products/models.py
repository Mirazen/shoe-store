from django.db import models


class Product(models.Model):
    article = models.CharField(max_length=100, verbose_name="Артикул")
    name = models.CharField(max_length=200, verbose_name="Название")
    price = models.IntegerField(verbose_name="Цена")
    provider = models.ForeignKey(
        "Provider", on_delete=models.CASCADE, verbose_name="Поставщик"
    )
    manufacturer = models.ForeignKey(
        "Manufacturer", on_delete=models.CASCADE, verbose_name="Производитель"
    )
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, verbose_name="Категория"
    )
    discount = models.IntegerField(default=0, verbose_name="Скидка")
    stock_quantity = models.IntegerField(default=0, verbose_name="Остаток")
    description = models.TextField(blank=True, verbose_name="Описание")
    image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name

    def get_discount_price(self):
        if self.discount > 0:
            return round(self.price * (100 - self.discount) / 100, 2)
        return self.price

    def has_discount(self):
        return self.discount > 0

    def has_large_discount(self):
        return self.discount > 15

    def is_out_of_stock(self):
        return self.stock_quantity == 0


class Provider(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Поставщик"
        verbose_name_plural = "Поставщики"


class Manufacturer(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Производитель"
        verbose_name_plural = "Производители"


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
