from .views import ProductList
from django.urls import path

app_name = 'blog_api'

urlpatterns = [
    path('', ProductList.as_view({'get': 'list', 'post': 'create'})),
    path('<slug:pk>/', ProductList.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('search/', ProductList.as_view({'get': 'retrieve'})),
]