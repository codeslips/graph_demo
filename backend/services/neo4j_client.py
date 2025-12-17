"""
Neo4j client service.

Provides connection management and query execution for Neo4j.
"""

import logging
from contextlib import contextmanager
from typing import Any, Generator

from django.conf import settings
from neo4j import GraphDatabase, Driver, Session

logger = logging.getLogger(__name__)


class Neo4jClient:
    """
    Neo4j database client with connection pooling.

    Usage:
        client = Neo4jClient()
        with client.session() as session:
            result = session.run("MATCH (n) RETURN n LIMIT 10")
            ...
        client.close()

    Or as context manager:
        with Neo4jClient() as client:
            with client.session() as session:
                ...
    """

    _instance: "Neo4jClient | None" = None
    _driver: Driver | None = None

    def __new__(cls) -> "Neo4jClient":
        """Singleton pattern for connection pooling."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize Neo4j client with settings from Django."""
        if self._driver is None:
            self.uri = getattr(settings, "NEO4J_URI", "bolt://localhost:7687")
            self.user = getattr(settings, "NEO4J_USER", "neo4j")
            self.password = getattr(settings, "NEO4J_PASSWORD", "password123")
            self._connect()

    def _connect(self) -> None:
        """Establish connection to Neo4j."""
        try:
            self._driver = GraphDatabase.driver(
                self.uri,
                auth=(self.user, self.password),
                max_connection_lifetime=3600,
                max_connection_pool_size=50,
            )
            # Verify connectivity
            self._driver.verify_connectivity()
            logger.info(f"Connected to Neo4j at {self.uri}")
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            raise

    @property
    def driver(self) -> Driver:
        """Get the Neo4j driver instance."""
        if self._driver is None:
            self._connect()
        return self._driver

    @contextmanager
    def session(self, **kwargs) -> Generator[Session, None, None]:
        """
        Get a Neo4j session as context manager.

        Args:
            **kwargs: Additional arguments to pass to driver.session()

        Yields:
            Neo4j Session instance
        """
        session = self.driver.session(**kwargs)
        try:
            yield session
        finally:
            session.close()

    def run_query(
        self,
        query: str,
        parameters: dict[str, Any] | None = None,
        **kwargs,
    ) -> list[dict[str, Any]]:
        """
        Execute a Cypher query and return results as list of dicts.

        Args:
            query: Cypher query string
            parameters: Query parameters
            **kwargs: Additional session arguments

        Returns:
            List of records as dictionaries
        """
        with self.session(**kwargs) as session:
            result = session.run(query, parameters or {})
            return [record.data() for record in result]

    def run_write_query(
        self,
        query: str,
        parameters: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Execute a write query within a transaction.

        Args:
            query: Cypher query string
            parameters: Query parameters

        Returns:
            Query summary as dictionary
        """
        with self.session() as session:

            def _write_tx(tx):
                result = tx.run(query, parameters or {})
                return result.consume()

            summary = session.execute_write(_write_tx)
            return {
                "nodes_created": summary.counters.nodes_created,
                "nodes_deleted": summary.counters.nodes_deleted,
                "relationships_created": summary.counters.relationships_created,
                "relationships_deleted": summary.counters.relationships_deleted,
                "properties_set": summary.counters.properties_set,
            }

    def close(self) -> None:
        """Close the Neo4j driver connection."""
        if self._driver:
            self._driver.close()
            self._driver = None
            Neo4jClient._instance = None
            logger.info("Neo4j connection closed")

    def __enter__(self) -> "Neo4jClient":
        """Enter context manager."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit context manager."""
        self.close()

    def health_check(self) -> bool:
        """
        Check if Neo4j is accessible.

        Returns:
            True if connection is healthy, False otherwise
        """
        try:
            self.driver.verify_connectivity()
            return True
        except Exception as e:
            logger.error(f"Neo4j health check failed: {e}")
            return False


# Global client instance for convenience
def get_neo4j_client() -> Neo4jClient:
    """Get the singleton Neo4j client instance."""
    return Neo4jClient()
