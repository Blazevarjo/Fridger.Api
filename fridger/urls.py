from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path, reverse_lazy
from django.views.generic.base import RedirectView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from fridger.users.urls import api_urls as users_urls
from fridger.users.urls import frontend_urls

v1_urls = [
    path("", include(users_urls)),
    # Documentation
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(v1_urls)),
    path("", include(frontend_urls)),
    re_path(r"^$", RedirectView.as_view(url=reverse_lazy("swagger-ui"), permanent=False)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
