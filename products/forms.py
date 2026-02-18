from django import forms
from cart.models import CartItem


class AddToCartForm(forms.ModelForm):
    quantity = forms.IntegerField(min_value=1, initial=1, label="Количество")

    class Meta:
        model = CartItem
        fields = ["quantity"]
