from django.urls import path
from carSearchSite import views

app_name = "carSearch"
urlpatterns = [
    path("",views.CarSearchModel.as_view(),name="FP"),
    path('list/',views.carList,name='carList'),
    path('delInfo/<int:deleteqs>/<int:deleteimg>',views.deleteInfo,name='delInfo')
]
