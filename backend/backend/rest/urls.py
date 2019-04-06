from django.conf.urls import include, url
from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import page

router = SimpleRouter()
router.register("page", page.PageAPI, "page")

urlpatterns = [path("api/v1.0/", include((router.urls, "page"), namespace="v1.0"))]
