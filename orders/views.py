from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Order
from .forms import OrderForm
from products.views import AdminOnlyMixin


@login_required
def order_list(request):
    if request.user.role not in ["manager", "admin"]:
        return redirect("products:catalog")

    orders = Order.objects.select_related("customer", "pickup_point").all()
    return render(request, "orders/order_list.html", {"orders": orders})


class OrderCreateView(AdminOnlyMixin, CreateView):
    model = Order
    context_object_name = "order"
    form_class = OrderForm
    template_name = "orders/order_form.html"
    success_url = reverse_lazy("orders:order_list")


class OrderUpdateView(AdminOnlyMixin, UpdateView):
    model = Order
    context_object_name = "order"
    form_class = OrderForm
    template_name = "orders/order_form.html"
    success_url = reverse_lazy("orders:order_list")


class OrderDeleteView(AdminOnlyMixin, DeleteView):
    model = Order
    template_name = "orders/order_delete_confirm.html"
    success_url = reverse_lazy("orders:order_list")
