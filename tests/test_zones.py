import pytest
from fastapi import status


class TestZoneCreation:
    def test_create_zone_success(self, client):
        response = client.post("/api/v1/zones/", json={"nom": "Paris", "code_postal": "75001"})
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["nom"] == "Paris"
        assert data["code_postal"] == "75001"

    def test_create_zone_duplicate_postal_code(self, client, sample_zone):
        response = client.post("/api/v1/zones/", json={"nom": "New Paris", "code_postal": "75001"})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "already exists" in response.json()["detail"]

    def test_create_zone_missing_nom(self, client):
        response = client.post("/api/v1/zones/", json={"code_postal": "75001"})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_zone_missing_code_postal(self, client):
        response = client.post("/api/v1/zones/", json={"nom": "Paris"})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_zone_empty_nom(self, client):
        response = client.post("/api/v1/zones/", json={"nom": "", "code_postal": "75001"})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_zone_empty_nom(self, client):
        response = client.post("/api/v1/zones/", json={"nom": "", "code_postal": "75001"})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestZoneRetrieval:
    def test_list_zones_empty(self, client):
        response = client.get("/api/v1/zones/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_list_zones_with_data(self, client, sample_zone):
        response = client.get("/api/v1/zones/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["nom"] == "Paris"

    def test_list_multiple_zones(self, client, db):
        from app.models import Zone
        for zone_data in [{"nom": "Paris", "code_postal": "75001"}, 
                          {"nom": "Lyon", "code_postal": "69001"}]:
            db.add(Zone(**zone_data))
        db.commit()
        response = client.get("/api/v1/zones/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 2

    def test_get_zone_by_id(self, client, sample_zone):
        response = client.get(f"/api/v1/zones/{sample_zone.id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == sample_zone.id
        assert data["nom"] == "Paris"

    def test_get_zone_not_found(self, client):
        response = client.get("/api/v1/zones/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_zone_invalid_id(self, client):
        response = client.get("/api/v1/zones/invalid")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestZoneUpdate:
    def test_update_zone_nom(self, client, sample_zone):
        response = client.put(f"/api/v1/zones/{sample_zone.id}", json={"nom": "Paris Updated"})
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["nom"] == "Paris Updated"
        assert data["code_postal"] == "75001"

    def test_update_zone_code_postal(self, client, sample_zone):
        response = client.put(f"/api/v1/zones/{sample_zone.id}", json={"code_postal": "75002"})
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["code_postal"] == "75002"

    def test_update_zone_multiple_fields(self, client, sample_zone):
        response = client.put(f"/api/v1/zones/{sample_zone.id}", 
                             json={"nom": "Paris Updated", "code_postal": "75003"})
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["nom"] == "Paris Updated"
        assert data["code_postal"] == "75003"

    def test_update_zone_not_found(self, client):
        response = client.put("/api/v1/zones/999", json={"nom": "Non Existent"})
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_zone_empty_body(self, client, sample_zone):
        response = client.put(f"/api/v1/zones/{sample_zone.id}", json={})
        assert response.status_code == status.HTTP_200_OK


class TestZoneDeletion:
    def test_delete_zone_success(self, client, sample_zone):
        response = client.delete(f"/api/v1/zones/{sample_zone.id}")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        verify = client.get(f"/api/v1/zones/{sample_zone.id}")
        assert verify.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_zone_not_found(self, client):
        response = client.delete("/api/v1/zones/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_nonexistent_zone(self, client, sample_zone):
        client.delete(f"/api/v1/zones/{sample_zone.id}")
        response = client.delete(f"/api/v1/zones/{sample_zone.id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
