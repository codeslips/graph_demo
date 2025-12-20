# -*- coding: utf-8 -*-
"""Tieba API endpoints."""

from ninja import Router

from ..models import TiebaComment, TiebaCreator, TiebaNote
from ..schemas.tieba import (
    TiebaCommentCreate,
    TiebaCommentOut,
    TiebaCommentUpdate,
    TiebaCreatorCreate,
    TiebaCreatorOut,
    TiebaCreatorUpdate,
    TiebaNoteCreate,
    TiebaNoteOut,
    TiebaNoteUpdate,
)
from .base import create_crud_router

# Create routers for each model
notes_router = create_crud_router(
    model=TiebaNote,
    create_schema=TiebaNoteCreate,
    update_schema=TiebaNoteUpdate,
    out_schema=TiebaNoteOut,
    tags=["Tieba - Notes"],
    time_field="publish_time",
)

comments_router = create_crud_router(
    model=TiebaComment,
    create_schema=TiebaCommentCreate,
    update_schema=TiebaCommentUpdate,
    out_schema=TiebaCommentOut,
    tags=["Tieba - Comments"],
    time_field="publish_time",
)

creators_router = create_crud_router(
    model=TiebaCreator,
    create_schema=TiebaCreatorCreate,
    update_schema=TiebaCreatorUpdate,
    out_schema=TiebaCreatorOut,
    tags=["Tieba - Creators"],
    time_field=None,
)

# Main Tieba router
router = Router(tags=["Tieba"])
router.add_router("/notes", notes_router)
router.add_router("/comments", comments_router)
router.add_router("/creators", creators_router)

