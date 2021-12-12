from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter(trailing_slash=False)
router.register("fridges-products", views.FridgeProductViewSet, basename="fridge-product")
router.register("fridges-history-products", views.FridgeProductHistoryViewSet, basename="fridge-history-product")
api_urls = router.urls
