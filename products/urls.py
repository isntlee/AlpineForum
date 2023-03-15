from django.urls import path
from django.views.generic import TemplateView

app_name = 'products'

urlpatterns = [
    path ('', TemplateView.as_view(template_name='products/index.html'))
]