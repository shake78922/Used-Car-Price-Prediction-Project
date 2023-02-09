from django.urls import path
from machineLearning import views

app_name="machineLearning"

urlpatterns = [
    path('',views.CarSearch.as_view(),name="model_2"),
    path('result/',views.result, name='result')
]
