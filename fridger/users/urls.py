from django.urls import include, path
from djoser.views import TokenCreateView, TokenDestroyView, UserViewSet
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter(trailing_slash=False)
router.register("friends", views.FriendViewSet, basename="friend")
router.register("users", views.UserDetailViewSet, basename="user")

auth_urls = [
    path("", UserViewSet.as_view({"post": "create"})),
    path(
        "/me",
        views.UpdateUserViewSet.as_view({"get": "me", "patch": "me", "delete": "me"}),
    ),
    path("/me/change-password", UserViewSet.as_view({"post": "set_password"})),
    path("/activate", UserViewSet.as_view({"post": "activation"})),
    path("/reset-password", UserViewSet.as_view({"post": "reset_password"})),
    path("/reset-password-confirm", UserViewSet.as_view({"post": "reset_password_confirm"})),
    path("/login", TokenCreateView.as_view()),
    path("/logout", TokenDestroyView.as_view()),
]

api_urls = [
    path("auth/users", include(auth_urls)),
    path("statistics", views.StatisticsView.as_view()),
]

api_urls += router.urls

frontend_urls = [
    path("activate/<slug:uid>/<slug:token>", views.activate_account, name="activate_account"),
    path("password-reset/<slug:uid>/<slug:token>", views.password_reset, name="password_reset"),
]
