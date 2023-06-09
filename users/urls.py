from django.urls import path
from . import views

app_name = "urls"

urlpatterns = [
    path("<int:user_id>/profile", views.update_profile, name="profile"),
    path("register", views.register, name="register")
]
