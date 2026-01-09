"""
Test cases for Zone API endpoints.
"""
import pytest
from fastapi import status


class TestZoneCreation:
    """Tests for zone creation endpoint."""

    def test_create_zone_success(self, client):
        """Test successful zone creation."""
        zone_data = {
            "nom": "Paris",
            "code_postal": "75001"
        }
        response = client.post("/api/v1/zones/", json=zone_data)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["nom"] == "Paris"
        assert data["code_postal"] == "75001"
        assert "id" in data

    def test_create_zone_duplicate_postal_code(self, client, sample_zone):
        """Test that creating a zone with duplicate postal code fails."""
        zone_data = {
            "nom": "New Paris",
            "code_postal": "75001"  # Same as sample_zone
        }
        response = client.post("/api/v1/zones/", json=zone_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        data = response.json()
        assert "already exists" in data["detail"]

    def test_create_zone_missing_nom(self, client):
        """Test zone creation with missing nom field."""
        zone_data = {
            "code_postal": "75001"
        }
        response = client.post("/api/v1/zones/", json=zone_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_zone_missing_code_postal(self, client):
        """Test zone creation with missing code_postal field."""
        zone_data = {
            "nom": "Paris"
        }
        response = client.post("/api/v1/zones/", json=zone_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_zone_empty_nom(self, client):
        """Test zone creation with empty nom field."""
        zone_data = {
            "nom": "",
            "code_postal": "75001"
        }
        response = client.post("/api/v1/zones/", json=zone_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestZoneRetrieval:
    """Tests for zone retrieval endpoints."""

    def test_list_zones_empty(self, client):
        """Test listing zones when database is empty."""
        response = client.get("/api/v1/zones/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data == []

    def test_list_zones_with_data(self, client, sample_zone):
        """Test listing zones returns all zones."""
        response = client.get("/api/v1/zones/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["nom"] == "Paris"
        assert data[0]["code_postal"] == "75001"

    def test_list_multiple_zones(self, client, db):
        """Test listing multiple zones."""
        from app.models import Zone
        
        zones_data = [
            {"nom": "Paris", "code_postal": "75001"},
            {"nom": "Lyon", "code_postal": "69001"},
            {"nom": "Marseille", "code_postal": "13001"}
        ]
        
        for zone_data in zones_data:
            zone = Zone(**zone_data)
            db.add(zone)
        db.commit()
        
        response = client.get("/api/v1/zones/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 3

    def test_get_zone_by_id(self, client, sample_zone):
        """Test retrieving a zone by ID."""
        response = client.get(f"/api/v1/zones/{sample_zone.id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == sample_zone.id
        assert data["nom"] == "Paris"

    def test_get_zone_not_found(self, client):
        """Test retrieving a zone that doesn't exist."""
        response = client.get("/api/v1/zones/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert "not found" in data["detail"]

    def test_get_zone_invalid_id(self, client):
        """Test retrieving a zone with invalid ID format."""
        response = client.get("/api/v1/zones/invalid")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestZoneUpdate:
    """Tests for zone update endpoint."""

    def test_update_zone_nom(self, client, sample_zone):
        """Test updating zone nom field."""
        update_data = {"nom": "Paris Updated"}
        response = client.put(f"/api/v1/zones/{sample_zone.id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["nom"] == "Paris Updated"
        assert data["code_postal"] == "75001"  # Should remain unchanged

    def test_update_zone_code_postal(self, client, sample_zone):
        """Test updating zone code_postal field."""
        update_data = {"code_postal": "75002"}
        response = client.put(f"/api/v1/zones/{sample_zone.id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["code_postal"] == "75002"
        assert data["nom"] == "Paris"  # Should remain unchanged

    def test_update_zone_multiple_fields(self, client, sample_zone):
        """Test updating multiple zone fields."""
        update_data = {
            "nom": "Paris Updated",
            "code_postal": "75003"
        }
        response = client.put(f"/api/v1/zones/{sample_zone.id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["nom"] == "Paris Updated"
        assert data["code_postal"] == "75003"

    def test_update_zone_not_found(self, client):
        """Test updating a zone that doesn't exist."""
        update_data = {"nom": "Non Existent"}
        response = client.put("/api/v1/zones/999", json=update_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_zone_empty_body(self, client, sample_zone):
        """Test updating zone with empty body."""
        response = client.put(f"/api/v1/zones/{sample_zone.id}", json={})
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        # Fields should remain unchanged
        assert data["nom"] == "Paris"
        assert data["code_postal"] == "75001"


class TestZoneDeletion:
    """Tests for zone deletion endpoint."""

    def test_delete_zone_success(self, client, sample_zone):
        """Test successful zone deletion."""
        response = client.delete(f"/api/v1/zones/{sample_zone.id}")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify zone is deleted
        verify_response = client.get(f"/api/v1/zones/{sample_zone.id}")
        assert verify_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_zone_not_found(self, client):
        """Test deleting a zone that doesn't exist."""
        response = client.delete("/api/v1/zones/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_nonexistent_zone(self, client, sample_zone):
        """Test deleting the same zone twice."""
        # First deletion
        response1 = client.delete(f"/api/v1/zones/{sample_zone.id}")
        assert response1.status_code == status.HTTP_204_NO_CONTENT
        
        # Second deletion should fail
        response2 = client.delete(f"/api/v1/zones/{sample_zone.id}")
        assert response2.status_code == status.HTTP_404_NOT_FOUND
