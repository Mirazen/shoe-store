from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path("", views.catalog, name="catalog"),
    path("add-to-cart/<int:product_pk>/", views.add_to_cart, name="add_to_cart"),
    path("create/", views.ProductCreateView.as_view(), name="product_create"),
    path("edit/<int:pk>/", views.ProductUpdateView.as_view(), name="product_edit"),
    path("delete/<int:pk>/", views.ProductDeleteView.as_view(), name="product_delete"),
]
