from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.db.models import Q
from products.models import Product
from .serializers import ProductSerializer


class ProductList(viewsets.ViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['description'] 

    def custom_filter(self, queryset):
        search_param = self.request.query_params.get('search')
        if search_param:
            queryset = queryset.filter(Q(description__icontains=search_param))
        return queryset

    def list(self, request):
        queryset = self.custom_filter(self.queryset)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, **kwargs):
        item = self.kwargs.get('pk')
        product = get_object_or_404(self.queryset, slug=item)
        serializer = self.serializer_class(product)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return ValidationError(serializer.errors)

    def update(self, request, pk=None):
        product = get_object_or_404(self.queryset, slug=pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return ValidationError(serializer.errors)
        
    def destroy(self, request, pk=None):
        product = get_object_or_404(self.queryset, slug=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
