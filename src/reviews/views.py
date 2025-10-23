from rest_framework import viewsets, permissions
from drf_spectacular.utils import extend_schema_view, extend_schema
from .models import Review
from .serializers import ReviewSerializer

@extend_schema_view(
    list=extend_schema(tags=["Reviews"]),
    retrieve=extend_schema(tags=["Reviews"]),
    create=extend_schema(tags=["Reviews"]),
    update=extend_schema(tags=["Reviews"]),
    partial_update=extend_schema(tags=["Reviews"]),
    destroy=extend_schema(tags=["Reviews"]),
)
class ReviewViewSet(viewsets.ModelViewSet):
    """Отзывы к объявлениям"""
    queryset = Review.objects.all().order_by("-created_at")
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
