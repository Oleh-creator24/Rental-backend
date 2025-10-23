from django.contrib import admin
from django.urls import path, include
from rest_framework_nested import routers
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from config.admin_dashboard import custom_admin_site
from listings.views import ListingViewSet
from bookings.views import BookingViewSet
from reviews.views import ReviewViewSet
from stats.views import StatsViewSet

# 🔹 импорт кастомных JWT-классов
from users.auth_views import CustomTokenObtainPairView, CustomTokenRefreshView

# --- Основные роутеры ---
router = routers.DefaultRouter()
router.register(r"listings", ListingViewSet, basename="listing")
router.register(r"bookings", BookingViewSet, basename="booking")
router.register(r"stats", StatsViewSet, basename="stats")

# --- Вложенные роутеры для отзывов ---
listings_router = routers.NestedDefaultRouter(router, r"listings", lookup="listing")
listings_router.register(r"reviews", ReviewViewSet, basename="listing-reviews")

urlpatterns = [
    path("admin/", custom_admin_site.urls),
    path("api/", include("src.api_router")),

    # --- AUTH (JWT endpoints) ---
    path("api/v1/auth/login/", CustomTokenObtainPairView.as_view(), name="auth-login"),
    path("api/v1/auth/refresh/", CustomTokenRefreshView.as_view(), name="auth-refresh"),

    # --- USERS ---
    path("api/v1/users/", include("users.urls")),

    # --- API ресурсы ---
    path("api/v1/", include(router.urls)),
    path("api/v1/", include(listings_router.urls)),

    # --- Документация ---
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/v1/schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/v1/schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
