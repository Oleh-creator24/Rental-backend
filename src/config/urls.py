from django.contrib import admin
from django.urls import path, include
from rest_framework_nested import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from listings.views import ListingViewSet
from bookings.views import BookingViewSet
from reviews.views import ReviewViewSet
from stats.views import StatsViewSet
from users.auth_views import CustomTokenObtainPairView, CustomTokenRefreshView

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static
from pathlib import Path


# --- Основной роутер ---
router = routers.DefaultRouter()
router.register(r"listings", ListingViewSet, basename="listing")
router.register(r"bookings", BookingViewSet, basename="booking")
router.register(r"stats", StatsViewSet, basename="stats")

# --- Вложенные роутеры для отзывов ---
listings_router = routers.NestedDefaultRouter(router, r"listings", lookup="listing")
listings_router.register(r"reviews", ReviewViewSet, basename="listing-reviews")

# --- Основные URL ---
urlpatterns = [
    path("admin/", admin.site.urls),

    # === Пользователи ===
    path("api/v1/users/", include("users.urls")),

    # === Аутентификация ===
    path("api/v1/auth/login/", CustomTokenObtainPairView.as_view(), name="auth-login"),
    path("api/v1/auth/refresh/", CustomTokenRefreshView.as_view(), name="auth-refresh"),

    # === Автоматические маршруты ===
    path("api/v1/", include(router.urls)),
    path("api/v1/", include(listings_router.urls)),

    # === JWT стандартные ===
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # === Документация ===
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),

    # Основные API
    path('api/v1/', include('users.urls')),
    path('api/v1/', include('listings.urls')),
    path('api/v1/', include('bookings.urls')),
    path('api/v1/', include('reviews.urls')),
    path('api/v1/', include('stats.urls')),

    # Схема и Swagger UI
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/v1/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/v1/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

# --- Статика и медиа ---
BASE_DIR = Path(__file__).resolve().parent.parent.parent
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static("/media/", document_root=BASE_DIR / "media")
