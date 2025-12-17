"""
Base crawler class.

Provides common functionality for all crawlers.
"""

from abc import ABC, abstractmethod


class BaseCrawler(ABC):
    """Abstract base class for crawlers."""

    @abstractmethod
    def crawl(self, url: str) -> list:
        """Crawl the given URL and return parsed items."""
        pass

    @abstractmethod
    def parse(self, content: str) -> dict:
        """Parse HTML content and extract data."""
        pass

