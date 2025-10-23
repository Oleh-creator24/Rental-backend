from rest_framework.routers import DefaultRouter
from .views import RegionViewSet, CountryViewSet, CityViewSet

router = DefaultRouter()
router.register(r"regions", RegionViewSet)
router.register(r"countries", CountryViewSet)
router.register(r"cities", CityViewSet)

urlpatterns = router.urls
