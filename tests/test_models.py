import pytest
from app.models import Zone, ClientExpeditor, Destinataire, Livreur, Colis, HistoriqueStatut, StatutColis


class TestZoneModel:
    def test_zone_creation(self, db):
        zone = Zone(nom="Paris", code_postal="75001")
        db.add(zone)
        db.commit()
        assert zone.id is not None
        assert zone.nom == "Paris"

    def test_zone_repr(self, db):
        zone = Zone(nom="Paris", code_postal="75001")
        db.add(zone)
        db.commit()
        assert "Zone" in repr(zone)
        assert "Paris" in repr(zone)

    def test_zone_unique_postal_code(self, db):
        zone1 = Zone(nom="Paris", code_postal="75001")
        db.add(zone1)
        db.commit()
        
        zone2 = Zone(nom="Lyon", code_postal="75001")
        db.add(zone2)
        with pytest.raises(Exception):
            db.commit()


class TestClientExpeditorModel:
    def test_client_expeditor_creation(self, db):
        client = ClientExpeditor(
            nom="Dupont", prenom="Jean", email="jean@example.com",
            telephone="0123456789", adresse="123 Rue de la Paix"
        )
        db.add(client)
        db.commit()
        assert client.id is not None
        assert client.nom == "Dupont"

    def test_client_expeditor_repr(self, db):
        client = ClientExpeditor(
            nom="Dupont", prenom="Jean", email="jean@example.com",
            telephone="0123456789", adresse="123 Rue"
        )
        db.add(client)
        db.commit()
        assert "ClientExpeditor" in repr(client)

    def test_client_expeditor_email_unique(self, db):
        client1 = ClientExpeditor(
            nom="Dupont", prenom="Jean", email="jean@example.com",
            telephone="0123456789", adresse="123 Rue"
        )
        db.add(client1)
        db.commit()
        
        client2 = ClientExpeditor(
            nom="Martin", prenom="Pierre", email="jean@example.com",
            telephone="0987654321", adresse="456 Rue"
        )
        db.add(client2)
        with pytest.raises(Exception):
            db.commit()


class TestDestinataireModel:
    def test_destinataire_creation(self, db):
        dest = Destinataire(
            nom="Martin", prenom="Pierre", email="pierre@example.com",
            telephone="0987654321", adresse="456 Rue de la Paix"
        )
        db.add(dest)
        db.commit()
        assert dest.id is not None

    def test_destinataire_repr(self, db):
        dest = Destinataire(
            nom="Martin", prenom="Pierre", email="pierre@example.com",
            telephone="0987654321", adresse="456 Rue"
        )
        db.add(dest)
        db.commit()
        assert "Destinataire" in repr(dest)


class TestLivreurModel:
    def test_livreur_creation(self, db):
        zone = Zone(nom="Paris", code_postal="75001")
        db.add(zone)
        db.commit()
        
        livreur = Livreur(
            nom="Durand", prenom="Marc", telephone="0123456789",
            vehicule="Camionnette", zone_assignee_id=zone.id
        )
        db.add(livreur)
        db.commit()
        assert livreur.id is not None

    def test_livreur_repr(self, db):
        zone = Zone(nom="Paris", code_postal="75001")
        db.add(zone)
        db.commit()
        
        livreur = Livreur(
            nom="Durand", prenom="Marc", telephone="0123456789",
            vehicule="Camionnette", zone_assignee_id=zone.id
        )
        db.add(livreur)
        db.commit()
        assert "Livreur" in repr(livreur)


class TestStatutColis:
    def test_statut_colis_constants(self):
        assert StatutColis.CREE == "cree"
        assert StatutColis.COLLECTE == "collecte"
        assert StatutColis.EN_STOCK == "en_stock"
        assert StatutColis.EN_TRANSIT == "en_transit"
        assert StatutColis.LIVRE == "livre"

    def test_statut_colis_all_statuts(self):
        assert len(StatutColis.ALL_STATUTS) == 5
        assert all(status in StatutColis.ALL_STATUTS for status in 
                   [StatutColis.CREE, StatutColis.COLLECTE, StatutColis.EN_STOCK, 
                    StatutColis.EN_TRANSIT, StatutColis.LIVRE])


class TestColisModel:
    def test_colis_creation(self, db):
        zone = Zone(nom="Paris", code_postal="75001")
        db.add(zone)
        db.commit()
        
        client = ClientExpeditor(
            nom="Dupont", prenom="Jean", email="jean@example.com",
            telephone="0123456789", adresse="123 Rue"
        )
        db.add(client)
        db.commit()
        
        dest = Destinataire(
            nom="Martin", prenom="Pierre", email="pierre@example.com",
            telephone="0987654321", adresse="456 Rue"
        )
        db.add(dest)
        db.commit()
        
        colis = Colis(
            description="Colis fragile", poids=2.5, id_client_expeditor=client.id,
            id_destinataire=dest.id, id_zone=zone.id, ville_destination="Lyon"
        )
        db.add(colis)
        db.commit()
        assert colis.id is not None
        assert colis.statut == StatutColis.CREE

    def test_colis_repr(self, db):
        zone = Zone(nom="Paris", code_postal="75001")
        db.add(zone)
        db.commit()
        
        client = ClientExpeditor(
            nom="Dupont", prenom="Jean", email="jean@example.com",
            telephone="0123456789", adresse="123 Rue"
        )
        db.add(client)
        db.commit()
        
        dest = Destinataire(
            nom="Martin", prenom="Pierre", email="pierre@example.com",
            telephone="0987654321", adresse="456 Rue"
        )
        db.add(dest)
        db.commit()
        
        colis = Colis(
            description="Colis fragile", poids=2.5, id_client_expeditor=client.id,
            id_destinataire=dest.id, id_zone=zone.id, ville_destination="Lyon"
        )
        db.add(colis)
        db.commit()
        assert "Colis" in repr(colis)


class TestHistoriqueStatutModel:
    def test_historique_statut_creation(self, db):
        zone = Zone(nom="Paris", code_postal="75001")
        db.add(zone)
        db.commit()
        
        client = ClientExpeditor(
            nom="Dupont", prenom="Jean", email="jean@example.com",
            telephone="0123456789", adresse="123 Rue"
        )
        db.add(client)
        db.commit()
        
        dest = Destinataire(
            nom="Martin", prenom="Pierre", email="pierre@example.com",
            telephone="0987654321", adresse="456 Rue"
        )
        db.add(dest)
        db.commit()
        
        colis = Colis(
            description="Colis", poids=1.0, id_client_expeditor=client.id,
            id_destinataire=dest.id, id_zone=zone.id, ville_destination="Lyon"
        )
        db.add(colis)
        db.commit()
        
        historique = HistoriqueStatut(
            id_colis=colis.id, ancien_statut=StatutColis.CREE,
            nouveau_statut=StatutColis.COLLECTE, notes="Colis collecté"
        )
        db.add(historique)
        db.commit()
        assert historique.id is not None
        assert historique.ancien_statut == StatutColis.CREE
