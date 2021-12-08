from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter(trailing_slash=False)
router.register("fridges", views.FridgeViewSet, basename="fridge")
api_urls = router.urls
