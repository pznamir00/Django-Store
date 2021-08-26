import django_filters as filters
from django_filters.filters import OrderingFilter
from .models import Product



class ProductFilter(filters.FilterSet):
    min_date = filters.DateFilter('created_at', lookup_expr=('gt'))
    max_date = filters.DateFilter('created_at', lookup_expr=('lt'))
    min_price = filters.NumberFilter('price', lookup_expr=('gt'))
    max_price = filters.NumberFilter('price', lookup_expr=('lt'))
    color = filters.NumberFilter('color')
    brand = filters.NumberFilter('brand')
    order_by_field = 'ordering'
    ordering = OrderingFilter(
        fields = (
            ('price', 'price'),
            ('created_at', 'created_at'),
            ('name', 'name')
        )
    )

    class Meta:
        model = Product
        fields = ('min_date', 'max_date', 'min_price', 'max_price', 'color', 'brand')