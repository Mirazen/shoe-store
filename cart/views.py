from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem


@login_required
def view_cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total = sum(item.get_total_price() for item in cart_items)

    return render(request, "cart/cart.html", {"products": cart_items, "total": total})


@login_required
def remove_from_cart(request, product_id):
    if request.method == "POST":
        cart = request.user.cart
        cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
        cart_item.delete()

    return redirect("cart:cart")
