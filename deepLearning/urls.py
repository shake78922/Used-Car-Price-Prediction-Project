from django.urls import path
from deepLearning import views

app_name = "deepLearning"

urlpatterns = [
    path("",views.UploadImage.as_view(),name="model_1"),
    # path('upload_images/', views.UploadImage.as_view(),name='upload_images_url'),
    
]
