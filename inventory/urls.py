from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "inventory"
urlpatterns = [
                  # path("", views.IndexView.as_view(), name="index"),
                  # 1. Have item information in database
                  path("get_item_info_by_code/<str:code>", views.getItemInfoByCode, name="get_item_info_by_code"),

                  # 2. Have item BO number on hand, scrap in amz .env.production
                  path("scrap_info_by_bo_code/<str:code>", views.scrapInfoByBOCode, name="scrap_info_by_bo_code"),

                  # 3. Have item amz url on hand
                  path("scrap_info_by_url", views.scrapInfoByURL, name="scrap_info_by_url"),

                  path("scrap_info_by_num_code/<str:code>", views.scrapInfoByNumCode, name="scrap_info_by_num_code"),

                  # Dowmload images by urls
                  # path("download_images_by_urls", views.DownloadImagesByUrlsView.    as_view(), name="download_images_by_urls"),

                  # CRUD item
                  path("add_new_item", views.AddNewItemView.as_view(), name="add_new_item"),  # Post
                  path("delete_item/<int:pk>", views.deleteItem, name="delete_item"),  # Delete
                  path("update_item/<int:pk>", views.updateItem, name="update_item"),  # Put
                  path("get_item/<int:pk>", views.getItem, name="get_item"),  # Get
                  path("get_items", views.getItems, name="get_items"),  # Get
                  path("get_total_item", views.getTotalItems, name="get_total_item"),  # Get
                  path("export_items", views.exportItems, name="export_items"),  # Get
                  path("get_last_items/<int:staff_id>", views.getLastItems, name="get_last_items"),  # Get



                  # session, save case number
                  # Item list content
                  # path("get_status",views.GetStatusView.as_view(),name="get_status"),
                  # path("get_categories", views.GetCategoriesView.as_view(), name="get_categories"),
                  # path("get_sizes_by_category/<int:class_id>", views.GetSizesByCategoryView.as_view(), name="get_sizes_by_category"),
                  # path("get_colors_by_category", views.GetColorsByCategoryView.as_view(), name="get_colors_by_category"),

                  path("status", views.StatusView.as_view(), name="status"),
                  path("category", views.CategoryView.as_view(), name="category"),
                  path("image_upload", views.ImageUploadView.as_view(), name="image_upload"),
                  path("test_download_image", views.addImage, name="test_download_image"),
                  path("delete_image/<int:pk>", views.deleteImage, name="delete_image"),
                  path("get_next_lot_number/<int:auction>", views.getNextLotNumber, name="get_next_lot_number"),
                  path("get_available_sequences/<int:auction>", views.getAvailableSequences, name="get_available_sequences"),
                  path("upload_sold_products", views.uploadSoldProducts, name="upload_sold_products"),

    # Simple requests
              ]
