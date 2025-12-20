# -*- coding: utf-8 -*-
"""Zhihu API endpoints."""

from ninja import Router

from ..models import ZhihuComment, ZhihuContent, ZhihuCreator
from ..schemas.zhihu import (
    ZhihuCommentCreate,
    ZhihuCommentOut,
    ZhihuCommentUpdate,
    ZhihuContentCreate,
    ZhihuContentOut,
    ZhihuContentUpdate,
    ZhihuCreatorCreate,
    ZhihuCreatorOut,
    ZhihuCreatorUpdate,
)
from .base import create_crud_router

# Create routers for each model
contents_router = create_crud_router(
    model=ZhihuContent,
    create_schema=ZhihuContentCreate,
    update_schema=ZhihuContentUpdate,
    out_schema=ZhihuContentOut,
    tags=["Zhihu - Contents"],
    time_field="created_time",
)

comments_router = create_crud_router(
    model=ZhihuComment,
    create_schema=ZhihuCommentCreate,
    update_schema=ZhihuCommentUpdate,
    out_schema=ZhihuCommentOut,
    tags=["Zhihu - Comments"],
    time_field="publish_time",
)

creators_router = create_crud_router(
    model=ZhihuCreator,
    create_schema=ZhihuCreatorCreate,
    update_schema=ZhihuCreatorUpdate,
    out_schema=ZhihuCreatorOut,
    tags=["Zhihu - Creators"],
    time_field=None,
)

# Main Zhihu router
router = Router(tags=["Zhihu"])
router.add_router("/contents", contents_router)
router.add_router("/comments", comments_router)
router.add_router("/creators", creators_router)

