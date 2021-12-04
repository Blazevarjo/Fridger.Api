from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter(trailing_slash=False)
router.register("products", views.ProductViewSet)
api_urls = router.urls
