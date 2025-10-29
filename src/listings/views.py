#from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated
#from .permissions import IsLandlord

from rest_framework import viewsets, permissions, filters, decorators, response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import F, Count, Sum, Q
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema_view, extend_schema

from .models import Listing, ListingView
from stats.models import SearchHistory
from .serializers import ListingSerializer, ListingViewSerializer
from .filters import ListingFilter
#from common.permissions import IsOwnerOrReadOnly, IsLandlord
from rest_framework.permissions import IsAuthenticatedOrReadOnly


EXCHANGE_RATES = {
    "EUR": 1.0,
    "USD": 1.08,
    "GBP": 0.85,
    "CHF": 0.95,
    "PLN": 4.35,
    "CZK": 25.4,
}


@extend_schema_view(
    list=extend_schema(tags=["Listings"]),
    retrieve=extend_schema(tags=["Listings"]),
    create=extend_schema(tags=["Listings"]),
    update=extend_schema(tags=["Listings"]),
    partial_update=extend_schema(tags=["Listings"]),
    destroy=extend_schema(tags=["Listings"]),
    search_trends=extend_schema(tags=["Listings"], summary="Популярные поисковые запросы"),
)
class ListingViewSet(viewsets.ModelViewSet):
    """CRUD для объявлений (жильё)"""

    queryset = Listing.objects.all().order_by("-created_at")
    serializer_class = ListingSerializer

    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ListingFilter
    search_fields = ["title", "description", "city", "country", "street"]
    ordering_fields = ["price", "created_at", "view_count"]

    # -------------------------------------
    # 🔹 Создание и редактирование объявлений
    # -------------------------------------
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):

        return [IsAuthenticatedOrReadOnly()]

    # -------------------------------------
    # 🔹 Просмотр объявления (увеличиваем счётчик + логируем просмотр)
    # -------------------------------------
    def retrieve(self, request, *args, **kwargs):
        listing = self.get_object()

        user = request.user if request.user.is_authenticated else None
        ip = self.get_client_ip(request)

        # Запись в историю просмотров
        ListingView.objects.create(listing=listing, user=user, ip_address=ip)

        # Увеличение счётчика
        listing.view_count = F("view_count") + 1
        listing.save(update_fields=["view_count"])

        return super().retrieve(request, *args, **kwargs)

    def get_client_ip(self, request):
        """Определяет IP пользователя"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        return x_forwarded_for.split(",")[0] if x_forwarded_for else request.META.get("REMOTE_ADDR")

    # -------------------------------------
    # 🔹 Фильтрация и поиск объявлений
    # -------------------------------------
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.annotate(review_count=Count("reviews"))
        query = self.request.query_params.get("search")
        min_price = self.request.query_params.get("min_price")
        max_price = self.request.query_params.get("max_price")
        country = self.request.query_params.get("country")
        currency = self.request.query_params.get("currency")
        available = self.request.query_params.get("is_available")

        # Фильтры
        if country:
            qs = qs.filter(country__icontains=country)
        if currency:
            qs = qs.filter(price_currency=currency)
        if available is not None:
            qs = qs.filter(is_available=(available.lower() == "true"))
        if min_price:
            qs = qs.filter(price__gte=min_price)
        if max_price:
            qs = qs.filter(price__lte=max_price)


        if query:
            user = self.request.user if self.request.user.is_authenticated else None
            record, created = SearchHistory.objects.get_or_create(
                user=user,
                query=query,
                defaults={"count": 1},
            )
            if not created:
                record.count = F("count") + 1
                record.save(update_fields=["count"])

            # Фильтруем объявления по ключевому слову
            qs = qs.filter(Q(title__icontains=query) | Q(description__icontains=query))

        return qs

    # -------------------------------------
    # 🔹 История просмотров объявления
    # -------------------------------------
    @decorators.action(detail=True, methods=["get"], permission_classes=[permissions.IsAuthenticated])
    def views(self, request, pk=None):
        """Возвращает историю просмотров конкретного объявления"""
        listing = self.get_object()
        views = listing.views.select_related("user").all()
        serializer = ListingViewSerializer(views, many=True)
        return response.Response(serializer.data)

    # -------------------------------------
    # 🔹 Популярные поисковые запросы
    # -------------------------------------
    @decorators.action(detail=False, methods=["get"], url_path="search-trends")
    def search_trends(self, request):
        """Возвращает 20 самых популярных поисковых запросов"""
        top = (
            SearchHistory.objects.values("query")
            .annotate(total=Sum("count"))
            .order_by("-total")[:20]
        )
        return Response(top)

    @decorators.action(detail=True, methods=["get"], permission_classes=[permissions.IsAuthenticated])
    def views(self, request, pk=None):
        """Возвращает историю просмотров конкретного объявления"""
        listing = self.get_object()
        views = listing.views.select_related("user").all()
        serializer = ListingViewSerializer(views, many=True)
        return response.Response(serializer.data)