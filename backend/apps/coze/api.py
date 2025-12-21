"""
Django Ninja API routes for Coze chat.
"""

from django.http import StreamingHttpResponse
from ninja import Router

from .schemas import ChatRequest, ErrorResponse
from .services import CozeConfigError, coze_service

router = Router(tags=["Coze Chat"])


@router.post(
    "/chat",
    response={400: ErrorResponse, 500: ErrorResponse},
    summary="Chat with Coze AI bot",
)
def chat(request, payload: ChatRequest):
    """
    Send a message to the Coze AI bot and receive a streaming response.

    The response is returned as Server-Sent Events (SSE) for real-time display.
    """
    if not payload.message or not payload.message.strip():
        return 400, ErrorResponse(
            error="Invalid message",
            detail="Message cannot be empty",
        )

    try:
        # Create streaming response
        response = StreamingHttpResponse(
            coze_service.chat_stream(payload.message.strip()),
            content_type="text/event-stream",
        )
        response["Cache-Control"] = "no-cache"
        response["X-Accel-Buffering"] = "no"
        return response

    except CozeConfigError as e:
        return 500, ErrorResponse(
            error="Configuration error",
            detail=str(e),
        )

