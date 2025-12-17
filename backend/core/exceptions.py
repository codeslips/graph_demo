"""
Custom exceptions for ThePaper Graph.
"""


class ThePaperGraphError(Exception):
    """Base exception for the application."""

    pass


class CrawlError(ThePaperGraphError):
    """Exception raised during crawling operations."""

    pass


class Neo4jConnectionError(ThePaperGraphError):
    """Exception raised when Neo4j connection fails."""

    pass

