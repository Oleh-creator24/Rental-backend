from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema_view, extend_schema
from .models import ListingView, SearchQuery
from listings.models import Listing
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count

@extend_schema_view(
    top_listings=extend_schema(tags=["Stats"], summary="Топ-объявления"),
    top_queries=extend_schema(tags=["Stats"], summary="Популярные поиски"),
    add_view=extend_schema(tags=["Stats"], summary="Добавить просмотр объявления"),
    add_query=extend_schema(tags=["Stats"], summary="Добавить поисковый запрос"),
    summary=extend_schema(tags=["Stats"], summary="Сводная статистика за 7 дней"),
)
class StatsViewSet(viewsets.ViewSet):
    """Аналитика по просмотрам и запросам"""

    @action(detail=False, methods=["get"])
    def top_listings(self, request):
        data = Listing.objects.annotate(views=Count("listingview")).order_by("-views")[:10]
        return Response({"top_listings": [{"id": l.id, "title": l.title, "views": l.views} for l in data]})

    @action(detail=False, methods=["get"])
    def top_queries(self, request):
        data = SearchQuery.objects.values("query").annotate(count=Count("id")).order_by("-count")[:10]
        return Response({"top_queries": data})

    @action(detail=False, methods=["post"])
    def add_view(self, request):
        return Response({"status": "view recorded"})

    @action(detail=False, methods=["post"])
    def add_query(self, request):
        return Response({"status": "query recorded"})

    @action(detail=False, methods=["get"])
    def summary(self, request):
        now = timezone.now()
        week_ago = now - timedelta(days=7)
        total_views = ListingView.objects.count()
        total_queries = SearchQuery.objects.count()
        unique_users = ListingView.objects.values("user").distinct().count()

        data = {
            "total_views": total_views,
            "unique_users": unique_users,
            "total_queries": total_queries,
        }
        return Response(data)
