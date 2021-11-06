from django.urls import include, path
from djoser.views import UserViewSet

from .views import activate_account

urls = [
    path("", UserViewSet.as_view({"post": "create"})),
    path(
        "me/",
        UserViewSet.as_view({"get": "me", "put": "me", "patch": "me", "delete": "me"}),
    ),
    path("activate/", UserViewSet.as_view({"post": "activation"})),
    path("reset_password/", UserViewSet.as_view({"post": "reset_password"})),
    path("reset_password_confirm/", UserViewSet.as_view({"post": "reset_password_confirm"})),
    path("", include("djoser.urls.authtoken")),
]

frontend_urls = [
    path("activate/<slug:uid>/<slug:token>", activate_account, name="activate_account"),
]
