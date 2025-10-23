from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ListingListCreateView, ListingDetailView,ListingViewSet

router = DefaultRouter()
router.register(r"listings", ListingViewSet, basename="listing")

urlpatterns = [
    path("", ListingListCreateView.as_view(), name="listing-list-create"),
    path("<int:pk>/", ListingDetailView.as_view(), name="listing-detail"),
]
