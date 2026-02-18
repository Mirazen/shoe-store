from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("", views.order_list, name="order_list"),
    path("create/", views.OrderCreateView.as_view(), name="order_create"),
    path("edit/<int:pk>/", views.OrderUpdateView.as_view(), name="order_edit"),
    path("delete/<int:pk>/", views.OrderDeleteView.as_view(), name="order_delete"),
]
