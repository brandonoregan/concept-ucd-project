from django.urls import path
from . import views

urlpatterns = [
    path("inbox", views.inbox, name="inbox"),
    path("inbox/<str:user_username>/", views.inbox, name="inbox_with_user"),
    path("create_message", views.create_message, name="create_message"),
]
