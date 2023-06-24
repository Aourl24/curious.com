from django.urls import path
from .views import overviewPage,detailviewPage,itemDetail

urlpatterns = [
    path('',overviewPage,name='OverviewUrl'),
    path('<str:label>/<str:name>/model',detailviewPage,name='ModelDetail'),
    path('<int:id>/<str:label>/<str:model>/itemdetail',itemDetail,name='ItemDetailUrl')
]