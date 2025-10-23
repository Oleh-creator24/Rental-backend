from rest_framework import serializers
from .models import Listing,ListingView
from decimal import Decimal
from django.utils import timezone
import pytz

#  Условные курсы валют (можно заменить на API)
EXCHANGE_RATES = {
    "EUR": Decimal("1.0"),
    "USD": Decimal("1.08"),
    "GBP": Decimal("0.85"),
    "CHF": Decimal("0.95"),
    "PLN": Decimal("4.35"),
    "CZK": Decimal("25.4"),
}


class ListingSerializer(serializers.ModelSerializer):
    """
    Сериализатор для объявлений.
    Добавлены:
    - converted_price (конвертация валюты)
    - local_created_at (локальное время по ?tz=)
    """
    converted_price = serializers.SerializerMethodField(read_only=True)
    local_created_at = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Listing
        fields = [
            "id",
            "owner",
            "title",
            "description",
            "price",
            "price_currency",
            "converted_price",
            "is_available",
            "country",
            "city",
            "street",
            "house_number",
            "apartment_number",
            "view_count",
            "created_at",
            "local_created_at",
            "__all__",
        ]
        read_only_fields = ["id", "owner", "view_count", "created_at"]

    def get_converted_price(self, obj):
        """Возвращает цену в выбранной валюте (?currency=USD)"""
        request = self.context.get("request")
        if not request:
            return None

        target_currency = request.query_params.get("currency")
        if not target_currency or target_currency not in EXCHANGE_RATES:
            return None

        base_rate = EXCHANGE_RATES.get(obj.price_currency, Decimal("1.0"))
        target_rate = EXCHANGE_RATES[target_currency]

        try:
            converted = (obj.price / base_rate) * target_rate
        except Exception:
            return None

        return f"{converted.quantize(Decimal('0.01'))} {target_currency}"

    def get_local_created_at(self, obj):
        """Конвертирует created_at в локальный часовой пояс пользователя"""
        request = self.context.get("request")
        if not request:
            return obj.created_at.isoformat()

        tz_name = request.query_params.get("tz", "UTC")
        try:
            tz = pytz.timezone(tz_name)
            local_time = timezone.localtime(obj.created_at, tz)
            return local_time.isoformat()
        except Exception:
            return timezone.localtime(obj.created_at).isoformat()

class ListingViewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    listing = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ListingView
        fields = ["id", "listing", "user", "ip_address", "viewed_at"]