from django.urls import path
from .views import OrderView



urlpatterns = [
    path("", OrderView.as_view(), name="order"),
    path("<uuid:order_id>/", OrderView.as_view(), name="one-order"),
]


