from django.contrib import admin
from django.urls import path, include
from rest_framework_nested import routers
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

from listings.views import ListingViewSet
from bookings.views import BookingViewSet
from reviews.views import ReviewViewSet
from stats.views import StatsViewSet
from users.auth_views import CustomTokenObtainPairView, CustomTokenRefreshView

# --- Основной роутер ---
router = routers.DefaultRouter()
router.register(r"listings", ListingViewSet, basename="listing")
router.register(r"bookings", BookingViewSet, basename="booking")
router.register(r"stats", StatsViewSet, basename="stats")

# --- Вложенные роутеры для отзывов ---
listings_router = routers.NestedDefaultRouter(router, r"listings", lookup="listing")
listings_router.register(r"reviews", ReviewViewSet, basename="listing-reviews")

urlpatterns = [
    # --- Админка ---
    path("admin/", admin.site.urls),

    # --- JWT аутентификация ---
    path("api/v1/auth/login/", CustomTokenObtainPairView.as_view(), name="auth-login"),
    path("api/v1/auth/refresh/", CustomTokenRefreshView.as_view(), name="auth-refresh"),

    # --- Основные API-модули ---
    path("api/v1/users/", include("users.urls")),
    path("api/v1/listings/", include("listings.urls")),
    path("api/v1/bookings/", include("bookings.urls")),
    path("api/v1/reviews/", include("reviews.urls")),

    # --- Автоматические маршруты ViewSet’ов ---
    path("api/v1/", include(router.urls)),
    path("api/v1/", include(listings_router.urls)),

    # --- Документация API ---
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/v1/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/v1/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),

    # --- (опционально) глобальный API router ---
    # Убедись, что src/api_router.py существует и корректно подключает маршруты
    path("api/", include("src.api_router")),
]
