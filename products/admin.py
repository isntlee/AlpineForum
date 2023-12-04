from django.contrib import admin
from . import models


@admin.register(models.Product)
class ProducerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'image', 'active', 'category', 'producer')
    prepopulated_fields = {'slug': ('name',), }


admin.site.register(models.Category)