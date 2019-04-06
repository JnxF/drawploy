from django.conf.urls import url
from django.urls import include


urlpatterns = [
    url(r"", include(("backend.rest.urls", "backend"), namespace="api")),
]
