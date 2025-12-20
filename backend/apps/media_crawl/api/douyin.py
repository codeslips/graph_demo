# -*- coding: utf-8 -*-
"""Douyin API endpoints."""

from ninja import Router

from ..models import DouyinAweme, DouyinAwemeComment, DyCreator
from ..schemas.douyin import (
    DouyinAwemeCommentCreate,
    DouyinAwemeCommentOut,
    DouyinAwemeCommentUpdate,
    DouyinAwemeCreate,
    DouyinAwemeOut,
    DouyinAwemeUpdate,
    DyCreatorCreate,
    DyCreatorOut,
    DyCreatorUpdate,
)
from .base import create_crud_router

# Create routers for each model
awemes_router = create_crud_router(
    model=DouyinAweme,
    create_schema=DouyinAwemeCreate,
    update_schema=DouyinAwemeUpdate,
    out_schema=DouyinAwemeOut,
    tags=["Douyin - Awemes"],
    time_field="create_time",
)

comments_router = create_crud_router(
    model=DouyinAwemeComment,
    create_schema=DouyinAwemeCommentCreate,
    update_schema=DouyinAwemeCommentUpdate,
    out_schema=DouyinAwemeCommentOut,
    tags=["Douyin - Comments"],
    time_field="create_time",
)

creators_router = create_crud_router(
    model=DyCreator,
    create_schema=DyCreatorCreate,
    update_schema=DyCreatorUpdate,
    out_schema=DyCreatorOut,
    tags=["Douyin - Creators"],
    time_field=None,
)

# Main Douyin router
router = Router(tags=["Douyin"])
router.add_router("/awemes", awemes_router)
router.add_router("/comments", comments_router)
router.add_router("/creators", creators_router)

