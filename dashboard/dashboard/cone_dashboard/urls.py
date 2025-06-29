from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from cone_dashboard import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('emissions/',views.emissions, name='emissions'),
    path('testing/', views.testing, name='testing'),
    path('training_results/', views.training_results, name='training_results'),
    path('api/metrics/', views.metrics_data, name='metrics_data'),
    path('api/co2/yolo12/', views.co2_data_Yolo12, name='co2_yolo12'),
    path('api/co2/faster/', views.co2_data_Faster, name='co2_faster'),
    path('api/images/yolo/', views.yolo_images, name='yolo_images'),
    path('api/images/faster/', views.faster_rcnn_images, name='faster_images'),
    path('api/images/all/', views.all_results_images, name='all_images'),
    path('api/upload/', views.upload_test_image, name='upload_image'),
    path('api/status/', views.system_status, name='system_status'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)