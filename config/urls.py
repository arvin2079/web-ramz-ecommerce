from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # admin panel endpoint
    path("admin/", admin.site.urls),
    # native apps endpoints
    path("ecommerce/", include("ecommerce.urls")),
]
