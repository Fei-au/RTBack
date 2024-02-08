from django.urls import path
from . import views

app_name="inventory"
urlpatterns = [
        # path("", views.IndexView.as_view(), name="index"),
        # path("<int:pk>/", views.IndexView.as_view(), name="title"),
        # 1. Have item information in database
        path("get_item_info_by_code/<str:code>", views.getItemInfoByCode, name="get_item_info_by_code"),

        # 2. Have item BO number on hand, scrap in amz .env.production
        path("scrap_info_by_bo_code/<str:code>", views.scrapInfoByBOCode, name="scrap_info_by_bo_code"),

        # 3. Have item amz url on hand
        # path("scrap_info_by_url/<str:url>", views.scrapInfoByURL  , name="scrap_info_by_url"),

        # Dowmload images by urls
        # path("download_images_by_urls", views.DownloadImagesByUrlsView.    as_view(), name="download_images_by_urls"),

        # CRUD item
        path("add_new_item", views.addNewItem, name="add_new_item"), # Post
        path("delete_item/<int:pk>", views.deleteItem, name="delete_item"), # Delete
        path("update_item/<int:pk>", views.updateItem, name="update_item"),# Put
        path("get_item/<int:pk>", views.getItem, name="get_item"),# Get

        # session, save case number
        # Item list content
        path("get_status",views.GetStatusView.as_view(),name="get_status"),
        path("get_categories", views.GetCategoriesView.as_view(), name="get_categories"),
        path("get_sizes_by_category/<int:class_id>", views.GetSizesByCategoryView.as_view(), name="get_sizes_by_category"),
        path("get_colors_by_category", views.GetColorsByCategoryView.as_view(), name="get_colors_by_category"),

        # Simple requests
        path("<int:pk>/description/", views.DescriptionView.as_view(), name="description"),
        path("<int:item_id>/set_description/", views.set_description, name="set_description"),
        path("<int:pk>/status/", views.StatusView.as_view(), name="status"),
        path("<int:pk>/bo_code/", views.BoCodeView.as_view(), name="bo_code"),
        path("success/", views.SuccessView.as_view(), name="success"),
];