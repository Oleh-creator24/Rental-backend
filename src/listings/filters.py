
import django_filters as filters
from .models import Listing

class ListingFilter(filters.FilterSet):
    price_min = filters.NumberFilter(field_name="price", lookup_expr="gte")
    price_max = filters.NumberFilter(field_name="price", lookup_expr="lte")
    location  = filters.CharFilter(field_name="location", lookup_expr="icontains")
    is_available = filters.BooleanFilter()

    class Meta:
        model = Listing
        fields = ["is_available", "location", "price_min", "price_max"]
