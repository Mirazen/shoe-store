from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin

from cart.models import Cart, CartItem
from .models import Product
from .forms import ProductFilterForm, ProductForm


def add_to_cart(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)

    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        cart, _ = Cart.objects.get_or_create(user=request.user)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, product=product, defaults={"quantity": quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return redirect("cart:cart")

    return render(request, "products/add_to_cart.html", {"product": product})


def catalog(request):
    products = Product.objects.select_related(
        "category", "manufacturer", "provider"
    ).all()
    form = ProductFilterForm(request.GET or None)

    if form.is_valid():
        search = form.cleaned_data.get("search", "")
        if search:
            products = products.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )

        category = form.cleaned_data.get("category", "")
        if category:
            products = products.filter(category=category)

        manufacturer = form.cleaned_data.get("manufacturer", "")
        if manufacturer:
            products = products.filter(manufacturer=manufacturer)

        provider = form.cleaned_data.get("provider", "")
        if provider:
            products = products.filter(provider=provider)

        min_price = form.cleaned_data.get("min_price", "")
        max_price = form.cleaned_data.get("max_price", "")
        if min_price:
            products = products.filter(price__gte=min_price)
        if max_price:
            products = products.filter(price__lte=max_price)

        sort_by = form.cleaned_data.get("sort_by", "")
        if sort_by == "name":
            products = products.order_by("name")
        elif sort_by == "price_asc":
            products = products.order_by("price")
        elif sort_by == "price_desc":
            products = products.order_by("-price")
        elif sort_by == "discount":
            products = products.order_by("-discount")

    return render(
        request, "products/catalog.html", {"products": products, "form": form}
    )


class AdminOnlyMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == "admin"


class ProductCreateView(AdminOnlyMixin, CreateView):
    model = Product
    context_object_name = "product"
    form_class = ProductForm
    template_name = "products/product_form.html"
    success_url = reverse_lazy("products:catalog")


class ProductUpdateView(AdminOnlyMixin, UpdateView):
    model = Product
    context_object_name = "product"
    form_class = ProductForm
    template_name = "products/product_form.html"
    success_url = reverse_lazy("products:catalog")


class ProductDeleteView(AdminOnlyMixin, DeleteView):
    model = Product
    template_name = "products/product_delete_confirm.html"
    success_url = reverse_lazy("products:catalog")
