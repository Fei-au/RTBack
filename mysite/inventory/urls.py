from django.urls import path
from . import views

app_name="inventory"
urlpatterns = [
        path("", views.IndexView.as_view(), name="index"),
        path("<int:pk>/", views.IndexView.as_view(), name="title"),
        path("find_url_by_code", views.FindUrlByCode.as_view(), name="find_url_by_code"),
        path("scrap_info_by_url", views.ScrapInfoByUrlView.    as_view(), name="scrap_info_by_url"),
        path("download_images_by_urls", views.DownloadImagesByUrlsView.    as_view(), name="download_images_by_urls"),
        # CRUD item
        path("add_new_item", views.AddNewItemView.    as_view(), name="add_new_item"),
        path("<int:pk>/delete_item", views.DeleteItemView.as_view(), name="delete_item"),
        path("<int:pk>/update_item", views.UpdateItemView.as_view(), name="update_item"),
        path("<int:pk>/get_item", views.GetItemView.    as_view(), name="get_item"),

        # session, save case number
        # Item list content
        path("get_status",views.GetStatusView.as_View(),name="get_status"),
        path("get_classes", views.GetClassesView.as_View(), name="get_classes"),
        path("get_sizes_by_class", views.GetSizesByClassView.as_View(), name="get_sizes_by_class"),
        path("get_colors_by_class", views.GetColorsByClassView.as_View(), name="get_colors_by_class"),

        #
        path("<int:pk>/description/", views.DescriptionView.as_view(), name="description"),
        path("<int:item_id>/set_description/", views.set_description, name="set_description"),
        path("<int:pk>/status/", views.StatusView.as_view(), name="status"),
        path("<int:pk>/bo_code/", views.BoCodeView.as_view(), name="bo_code"),
        path("success/", views.SuccessView.as_view(), name="success"),
];