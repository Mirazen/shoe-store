from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path("remove/<int:product_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("", views.view_cart, name="cart"),
]
