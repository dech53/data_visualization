# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # 将不同视图绑定到不同路径
    path('data/', views.name_data, name='name_data'),  # 显示数据的页面
    path('map/', views.map_view, name='map_view'),  # 显示地图的页面
]
