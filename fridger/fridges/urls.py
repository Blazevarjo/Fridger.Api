from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter(trailing_slash=False)
router.register("fridges", views.FridgeViewSet, basename="fridge")
router.register("fridges-ownerships", views.FridgeOwnershipViewSet, basename="fridge-ownership")
api_urls = router.urls
