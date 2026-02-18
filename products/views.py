from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .forms import AddToCartForm
from cart.models import Cart, CartItem


# add_to_cart(request, product_pk=123)
def add_to_cart(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)  # pk='123'
    form = AddToCartForm(request.POST or None)

    if form.is_valid():
        cart, _ = Cart.objects.get_or_create(user=request.user)
        quantity = form.cleaned_data["quantity"]

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, product=product, defaults={"quantity": quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return redirect("cart:cart")

    return render(request, "add_to_cart.html", {"form": form, "product": product})


def catalog(request):
    products = Product.objects.all()
    return render(request, "catalog.html", {"products": products})
