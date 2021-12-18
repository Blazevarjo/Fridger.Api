from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter(trailing_slash=False)
router.register("shopping-lists", views.ShoppingListViewSet, basename="shopping-list")
router.register("shopping-lists-ownerships", views.ShoppingListOwnershipViewSet, basename="shopping-list-ownership")
router.register("shopping-lists-fragments", views.ShoppingListFragmentViewSet, basename="shopping-list-fragment")
api_urls = router.urls
