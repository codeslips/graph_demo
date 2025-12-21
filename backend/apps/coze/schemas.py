"""
Pydantic schemas for Coze API.
"""

from ninja import Schema


class ChatRequest(Schema):
    """Request schema for chat endpoint."""

    message: str


class ErrorResponse(Schema):
    """Error response schema."""

    error: str
    detail: str | None = None

