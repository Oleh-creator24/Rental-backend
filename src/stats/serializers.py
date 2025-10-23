from rest_framework import serializers
from .models import ListingView, SearchQuery
from listings.models import Listing


class ListingStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = ["id", "title", "view_count"]


class SearchQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchQuery
        fields = ["id", "query", "count", "user", "created_at"]
