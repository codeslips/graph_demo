# -*- coding: utf-8 -*-
"""Xiaohongshu (XHS) API endpoints."""

from ninja import Router

from ..models import XhsCreator, XhsNote, XhsNoteComment
from ..schemas.xhs import (
    XhsCreatorCreate,
    XhsCreatorOut,
    XhsCreatorUpdate,
    XhsNoteCommentCreate,
    XhsNoteCommentOut,
    XhsNoteCommentUpdate,
    XhsNoteCreate,
    XhsNoteOut,
    XhsNoteUpdate,
)
from .base import create_crud_router

# Create routers for each model
creators_router = create_crud_router(
    model=XhsCreator,
    create_schema=XhsCreatorCreate,
    update_schema=XhsCreatorUpdate,
    out_schema=XhsCreatorOut,
    tags=["XHS - Creators"],
    time_field=None,
)

notes_router = create_crud_router(
    model=XhsNote,
    create_schema=XhsNoteCreate,
    update_schema=XhsNoteUpdate,
    out_schema=XhsNoteOut,
    tags=["XHS - Notes"],
    time_field="time",
)

comments_router = create_crud_router(
    model=XhsNoteComment,
    create_schema=XhsNoteCommentCreate,
    update_schema=XhsNoteCommentUpdate,
    out_schema=XhsNoteCommentOut,
    tags=["XHS - Comments"],
    time_field="create_time",
)

# Main XHS router
router = Router(tags=["Xiaohongshu"])
router.add_router("/creators", creators_router)
router.add_router("/notes", notes_router)
router.add_router("/comments", comments_router)

