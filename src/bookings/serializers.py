
from rest_framework import serializers
from .models import Booking
from django.utils.translation import gettext_lazy as _

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["id", "start_date", "end_date", "status", "created_at", "listing", "user"]
        read_only_fields = ["id", "status", "created_at", "user"]

    def validate(self, attrs):
        start = attrs.get("start_date") or getattr(self.instance, "start_date", None)
        end   = attrs.get("end_date")   or getattr(self.instance, "end_date", None)
        listing = attrs.get("listing")  or getattr(self.instance, "listing", None)

        if not start or not end or not listing:
            return attrs

        if end <= start:
            raise serializers.ValidationError({"end_date": _("Must be after start_date")})

        # запрет перекрытия с уже APPROVED бронированиями
        if Booking.objects.filter(
            listing=listing,
            status="APPROVED",
            start_date__lt=end,
            end_date__gt=start
        ).exists():
            raise serializers.ValidationError(_("Dates overlap with an approved booking."))

        return attrs

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        validated_data.setdefault("status", "PENDING")
        return super().create(validated_data)
