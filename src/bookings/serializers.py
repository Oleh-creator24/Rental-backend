from rest_framework import serializers
from bookings.models import Booking
from listings.serializers import ListingSerializer
from users.serializers import UserSerializer


class BookingSerializer(serializers.ModelSerializer):
    tenant = UserSerializer(read_only=True)
    listing = ListingSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = [
            "id",
            "listing",
            "tenant",
            "start_date",
            "end_date",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
