from django.urls import path
from djoser.views import TokenCreateView, TokenDestroyView, UserViewSet

from . import views

urls = [
    path("", UserViewSet.as_view({"post": "create"})),
    path(
        "me/",
        UserViewSet.as_view({"get": "me", "put": "me", "patch": "me", "delete": "me"}),
    ),
    path("activate/", UserViewSet.as_view({"post": "activation"})),
    path("reset_password/", UserViewSet.as_view({"post": "reset_password"})),
    path("reset_password_confirm/", UserViewSet.as_view({"post": "reset_password_confirm"})),
    path("login/", TokenCreateView.as_view()),
    path("logout/", TokenDestroyView.as_view()),
]

frontend_urls = [
    path("activate/<slug:uid>/<slug:token>", views.activate_account, name="activate_account"),
    path("password-reset/<slug:uid>/<slug:token>", views.password_reset, name="password_reset"),
]
