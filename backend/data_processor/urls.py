
from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_file, name='upload_file'),
    path('api/infer/', views.api_infer_data_types, name='api_infer_data_types'),
]