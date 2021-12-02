import debug_toolbar
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

from fridger.fridges.urls import api_urls as fridges_urls
from fridger.users.urls import api_urls as users_urls
from fridger.users.urls import frontend_urls

v1_urls = [
    path("", include(fridges_urls), name="fridge"),
    path("", include(users_urls), name="user"),
    # Documentation
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(v1_urls)),
    path("", include(frontend_urls)),
    # Debugging
    path("__debug__/", include(debug_toolbar.urls)),
    re_path(r"^$", RedirectView.as_view(url=reverse_lazy("swagger-ui"), permanent=False)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
