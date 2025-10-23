from rest_framework_nested import routers
from listings.views import ListingViewSet
from reviews.views import ReviewViewSet

# основной роутер
router = routers.DefaultRouter()
router.register(r'listings', ListingViewSet)

# вложенный роутер для отзывов конкретного объявления
reviews_router = routers.NestedDefaultRouter(router, r'listings', lookup='listing')
reviews_router.register(r'reviews', ReviewViewSet, basename='listing-reviews')

urlpatterns = router.urls + reviews_router.urls
