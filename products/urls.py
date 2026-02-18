from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path("add-to-cart/<int:product_pk>/", views.add_to_cart, name="add_to_cart"),
    path("", views.catalog, name="catalog"),
]
