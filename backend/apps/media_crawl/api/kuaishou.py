# -*- coding: utf-8 -*-
"""Kuaishou API endpoints."""

from ninja import Router

from ..models import KuaishouVideo, KuaishouVideoComment
from ..schemas.kuaishou import (
    KuaishouVideoCommentCreate,
    KuaishouVideoCommentOut,
    KuaishouVideoCommentUpdate,
    KuaishouVideoCreate,
    KuaishouVideoOut,
    KuaishouVideoUpdate,
)
from .base import create_crud_router

# Create routers for each model
videos_router = create_crud_router(
    model=KuaishouVideo,
    create_schema=KuaishouVideoCreate,
    update_schema=KuaishouVideoUpdate,
    out_schema=KuaishouVideoOut,
    tags=["Kuaishou - Videos"],
    time_field="create_time",
)

comments_router = create_crud_router(
    model=KuaishouVideoComment,
    create_schema=KuaishouVideoCommentCreate,
    update_schema=KuaishouVideoCommentUpdate,
    out_schema=KuaishouVideoCommentOut,
    tags=["Kuaishou - Comments"],
    time_field="create_time",
)

# Main Kuaishou router
router = Router(tags=["Kuaishou"])
router.add_router("/videos", videos_router)
router.add_router("/comments", comments_router)

