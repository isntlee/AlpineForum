from django.urls import path
from django.views.generic import TemplateView
from products import views


app_name = 'products'

urlpatterns = [
    path ('', TemplateView.as_view(template_name='products/index.html')),
    path('download', views.download, name='download'),
    path('find_product', views.find_product, name='find_product'),
]