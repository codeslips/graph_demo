"""
URL configuration for ThePaper Graph project.
"""

from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI

from apps.crawl.api import router as crawl_router
from apps.graph.api import router as graph_router
from apps.media_crawl.api import router as media_router

api = NinjaAPI(
    title="ThePaper Graph API",
    version="1.0.0",
    description="API for web crawling and graph visualization",
)

# Register API routers
api.add_router("/crawl/", crawl_router)
api.add_router("/graph/", graph_router)
api.add_router("/media/", media_router)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", api.urls),
]

