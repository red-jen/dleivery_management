"""
Test cases for the main application endpoints.
"""
import pytest
from fastapi import status


class TestHealthEndpoint:
    """Tests for the health check endpoint."""

    def test_health_check_returns_ok(self, client):
        """Test that health endpoint returns OK status."""
        response = client.get("/health")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "ok"
        assert data["app"] == "YouExpress API"

    def test_health_check_response_schema(self, client):
        """Test that health endpoint returns correct response schema."""
        response = client.get("/health")
        data = response.json()
        assert "status" in data
        assert "app" in data


class TestRootEndpoint:
    """Tests for the root endpoint."""

    def test_root_endpoint_returns_welcome_message(self, client):
        """Test that root endpoint returns welcome message."""
        response = client.get("/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "message" in data
        assert "YouExpress API" in data["message"]

    def test_root_endpoint_has_version(self, client):
        """Test that root endpoint includes version info."""
        response = client.get("/")
        data = response.json()
        assert "version" in data

    def test_root_endpoint_has_docs_url(self, client):
        """Test that root endpoint includes docs URL."""
        response = client.get("/")
        data = response.json()
        assert "docs" in data


class TestAPIDocumentation:
    """Tests for API documentation endpoints."""

    def test_swagger_ui_available(self, client):
        """Test that Swagger UI documentation is available."""
        response = client.get("/docs")
        assert response.status_code == status.HTTP_200_OK

    def test_redoc_available(self, client):
        """Test that ReDoc documentation is available."""
        response = client.get("/redoc")
        assert response.status_code == status.HTTP_200_OK

    def test_openapi_schema_available(self, client):
        """Test that OpenAPI schema is available."""
        response = client.get("/openapi.json")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "openapi" in data
