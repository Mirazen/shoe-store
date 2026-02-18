from django import forms
from .models import Provider, Manufacturer, Category, Product


class ProductFilterForm(forms.Form):
    CHOICES = [
        ("name", "По названию"),
        ("price_asc", "Цена: по возрастанию"),
        ("price_desc", "Цена: по убыванию"),
        ("discount", "По скидке"),
    ]

    search = forms.CharField(
        required=False,
        label="Поиск",
        max_length=100,
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        label="Категория",
        empty_label="Все категории",
    )
    manufacturer = forms.ModelChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False,
        label="Производитель",
    )
    provider = forms.ModelChoiceField(
        queryset=Provider.objects.all(),
        required=False,
        label="Поставщик",
    )
    min_price = forms.IntegerField(required=False, label="Цена от")
    max_price = forms.IntegerField(required=False, label="Цена до")
    sort_by = forms.ChoiceField(choices=CHOICES, required=False, label="Сортировка")


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        widgets = {"description": forms.Textarea(attrs={"rows": 4})}
