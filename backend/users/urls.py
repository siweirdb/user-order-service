from django.urls import path
from .views import UserView



urlpatterns = [
    path("", UserView.as_view()),
    path("<uuid:user_id>/", UserView.as_view()),
]

