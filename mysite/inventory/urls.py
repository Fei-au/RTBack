from django.urls import path
from . import views

app_name="inventory"
urlpatterns = [
        path("", views.IndexView.as_view(), name="index"),
        path("<int:pk>/", views.TitleView.as_view(), name="title"),
        path("<int:pk>/description/", views.DescriptionView.as_view(), name="description"),
        path("<int:item_id>/set_description/", views.set_description, name="set_description"),
        path("<int:pk>/status/", views.StatusView.as_view(), name="status"),
        path("success/", views.SuccessView.as_view(), name="success"),
];