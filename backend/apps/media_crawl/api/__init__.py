# -*- coding: utf-8 -*-
"""Media Crawl API package - Main router."""

from ninja import Router

from .bilibili import router as bilibili_router
from .douyin import router as douyin_router
from .kuaishou import router as kuaishou_router
from .weibo import router as weibo_router
from .xhs import router as xhs_router
from .tieba import router as tieba_router
from .zhihu import router as zhihu_router

# Main media crawl router
router = Router(tags=["Media Crawl"])

# Mount platform-specific routers
router.add_router("/bilibili", bilibili_router)
router.add_router("/douyin", douyin_router)
router.add_router("/kuaishou", kuaishou_router)
router.add_router("/weibo", weibo_router)
router.add_router("/xhs", xhs_router)
router.add_router("/tieba", tieba_router)
router.add_router("/zhihu", zhihu_router)


@router.get("/status", tags=["Media Crawl"])
def status(request):
    """Check media crawl API status."""
    from django.conf import settings

    return {
        "enabled": getattr(settings, "MEDIA_CRAWL_ENABLED", True),
        "integration_enabled": getattr(
            settings, "MEDIA_CRAWL_INTEGRATION_ENABLED", False
        ),
        "platforms": [
            "bilibili",
            "douyin",
            "kuaishou",
            "weibo",
            "xhs",
            "tieba",
            "zhihu",
        ],
    }
