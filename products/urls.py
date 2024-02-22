from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'products'

urlpatterns = [
    path ('', TemplateView.as_view(template_name='products/index.html')),
    path('download', views.download_video, name='download_video'),
]