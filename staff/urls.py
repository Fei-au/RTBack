from django.urls import path
from . import views

app_name="staff"
urlpatterns = [
    path("create_user", views.creatUser, name="create_user"),
    path("create_staff", views.creatStaff, name="create_staff"),

    # login user
    path("login", views.loginUser, name="login"),
    path("login_admin", views.loginAdmin, name="login_admin"),
    path("get_next_item_number/<int:pk>", views.getNextItemNumber, name="get_next_item_number"),

]