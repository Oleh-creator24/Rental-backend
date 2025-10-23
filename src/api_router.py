from rest_framework.routers import DefaultRouter
from django.urls import path, include

from listings.views import ListingViewSet
from bookings.views import BookingViewSet
from reviews.views import ReviewViewSet
from users.views import RegisterView, MeView

router = DefaultRouter()
router.register(r"listings", ListingViewSet)
router.register(r"bookings", BookingViewSet, basename="booking")
router.register(r"reviews", ReviewViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("users/register/", RegisterView.as_view(), name="user-register"),
    path("users/me/", MeView.as_view(), name="user-me"),
]
