from django.urls import path
from . import views

app_name="staff"
urlpatterns = [
    path("create_user", views.creatUser, name="create_user"),
    path("create_staff", views.creatStaff, name="create_staff"),

    # login user
    path("login", views.loginUser, name="login"),

]