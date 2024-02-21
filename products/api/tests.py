from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from products.models import Category
from django.contrib.auth.models import User


class ProductTests(APITestCase):

    def test_view_products(self):
        url = reverse('products.api:listcreate')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_product(self):
       self.test_category = Category.objects.create(name='django')
       self.test_user = User.objects.create_user(
            username='test_user_1', password='123456789')
       data = {'name':'Product Title', 'producer': 1, 'active': True,
               'description':'Product description', 'slug':'product-slug'}
       url = reverse('products.api:listcreate')
       response = self.client.post(url, data, format='json')
       self.assertEqual(response.status_code, status.HTTP_201_CREATED)
