# -*- coding: utf-8 -*-
"""Weibo API endpoints."""

from ninja import Router

from ..models import WeiboCreator, WeiboNote, WeiboNoteComment
from ..schemas.weibo import (
    WeiboCreatorCreate,
    WeiboCreatorOut,
    WeiboCreatorUpdate,
    WeiboNoteCommentCreate,
    WeiboNoteCommentOut,
    WeiboNoteCommentUpdate,
    WeiboNoteCreate,
    WeiboNoteOut,
    WeiboNoteUpdate,
)
from .base import create_crud_router

# Create routers for each model
notes_router = create_crud_router(
    model=WeiboNote,
    create_schema=WeiboNoteCreate,
    update_schema=WeiboNoteUpdate,
    out_schema=WeiboNoteOut,
    tags=["Weibo - Notes"],
    time_field="create_time",
)

comments_router = create_crud_router(
    model=WeiboNoteComment,
    create_schema=WeiboNoteCommentCreate,
    update_schema=WeiboNoteCommentUpdate,
    out_schema=WeiboNoteCommentOut,
    tags=["Weibo - Comments"],
    time_field="create_time",
)

creators_router = create_crud_router(
    model=WeiboCreator,
    create_schema=WeiboCreatorCreate,
    update_schema=WeiboCreatorUpdate,
    out_schema=WeiboCreatorOut,
    tags=["Weibo - Creators"],
    time_field=None,
)

# Main Weibo router
router = Router(tags=["Weibo"])
router.add_router("/notes", notes_router)
router.add_router("/comments", comments_router)
router.add_router("/creators", creators_router)

