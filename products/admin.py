from django.contrib import admin
from . import models


@admin.register(models.Product)
class ProducerAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'description', 'image_url', 'active', 'category', 'producer')
    prepopulated_fields = {'slug': ('name',), }


admin.site.register(models.Category)