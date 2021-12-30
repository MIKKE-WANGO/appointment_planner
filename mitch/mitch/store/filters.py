import django_filters
from .models import Product

class CategoryFilter(django_filters.FilterSet):
        class Meta:
            model = Product
            fields = ["category"]
        
