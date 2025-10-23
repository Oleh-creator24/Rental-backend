from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "rating", "comment", "created_at", "user", "listing"]
        read_only_fields = ["id", "created_at", "user", "listing"]

    def create(self, validated_data):
        request = self.context["request"]
        listing_id = self.context["view"].kwargs.get("listing_pk")
        validated_data["listing_id"] = listing_id
        validated_data["user"] = request.user
        return super().create(validated_data)
