"""
Coze API service for chat functionality.
"""

import json
import uuid
from typing import Generator

import httpx
from django.conf import settings


class CozeConfigError(Exception):
    """Raised when Coze configuration is missing or invalid."""

    pass


class CozeService:
    """Service for interacting with the Coze API."""

    def __init__(self):
        self.pat = settings.COZE_PAT
        self.bot_id = settings.COZE_BOT_ID
        self.base_url = settings.COZE_API_BASE_URL

    def _validate_config(self) -> None:
        """Validate that required configuration is present."""
        if not self.pat:
            raise CozeConfigError("COZE_PAT environment variable is not set")
        if not self.bot_id:
            raise CozeConfigError("COZE_BOT_ID environment variable is not set")

    def _get_headers(self) -> dict:
        """Get headers for Coze API requests."""
        return {
            "Authorization": f"Bearer {self.pat}",
            "Content-Type": "application/json",
        }

    def chat_stream(self, message: str) -> Generator[str, None, None]:
        """
        Send a chat message and stream the response.

        Args:
            message: The user's message to send to the bot.

        Yields:
            SSE formatted event strings.
        """
        self._validate_config()

        user_id = str(uuid.uuid4())
        url = f"{self.base_url}/v3/chat"

        payload = {
            "bot_id": self.bot_id,
            "user_id": user_id,
            "stream": True,
            "auto_save_history": False,
            "additional_messages": [
                {
                    "role": "user",
                    "content": message,
                    "content_type": "text",
                }
            ],
        }

        try:
            with httpx.Client(timeout=60.0) as client:
                with client.stream(
                    "POST",
                    url,
                    headers=self._get_headers(),
                    json=payload,
                ) as response:
                    if response.status_code != 200:
                        error_text = response.read().decode()
                        yield f"event: error\ndata: {json.dumps({'error': f'Coze API error: {response.status_code}', 'detail': error_text})}\n\n"
                        return

                    for line in response.iter_lines():
                        if line:
                            # Forward the SSE line as-is
                            yield f"{line}\n"
                        else:
                            # Empty line marks end of an event
                            yield "\n"

        except httpx.TimeoutException:
            yield f"event: error\ndata: {json.dumps({'error': 'Request timeout', 'detail': 'The request to Coze API timed out'})}\n\n"
        except httpx.RequestError as e:
            yield f"event: error\ndata: {json.dumps({'error': 'Request failed', 'detail': str(e)})}\n\n"
        except Exception as e:
            yield f"event: error\ndata: {json.dumps({'error': 'Unexpected error', 'detail': str(e)})}\n\n"


# Singleton instance
coze_service = CozeService()

