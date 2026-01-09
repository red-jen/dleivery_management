"""
Test cases for database models.
"""
import pytest
from app.models import Zone, ClientExpeditor, Destinataire, Livreur, Colis, HistoriqueStatut, StatutColis


class TestZoneModel:
    """Tests for Zone model."""

    def test_zone_creation(self, db):
        """Test creating a zone."""
        zone = Zone(nom="Paris", code_postal="75001")
        db.add(zone)
        db.commit()
        
        assert zone.id is not None
        assert zone.nom == "Paris"
        assert zone.code_postal == "75001"

    def test_zone_repr(self, db):
        """Test Zone __repr__ method."""
        zone = Zone(nom="Paris", code_postal="75001")
        db.add(zone)
        db.commit()
        
        repr_str = repr(zone)
        assert "Zone" in repr_str
        assert "Paris" in repr_str

    def test_zone_unique_postal_code(self, db):
        """Test that postal code is unique."""
        zone1 = Zone(nom="Paris", code_postal="75001")
        db.add(zone1)
        db.commit()
        
        zone2 = Zone(nom="Lyon", code_postal="75001")
        db.add(zone2)
        
        with pytest.raises(Exception):  # Should raise IntegrityError
            db.commit()


class TestClientExpeditorModel:
    """Tests for ClientExpeditor model."""

    def test_client_expeditor_creation(self, db):
        """Test creating a client expeditor."""
        client = ClientExpeditor(
            nom="Dupont",
            prenom="Jean",
            email="jean@example.com",
            telephone="0123456789",
            adresse="123 Rue de la Paix, Paris"
        )
        db.add(client)
        db.commit()
        
        assert client.id is not None
        assert client.nom == "Dupont"
        assert client.prenom == "Jean"
        assert client.email == "jean@example.com"

    def test_client_expeditor_repr(self, db):
        """Test ClientExpeditor __repr__ method."""
        client = ClientExpeditor(
            nom="Dupont",
            prenom="Jean",
            email="jean@example.com",
            telephone="0123456789",
            adresse="123 Rue de la Paix"
        )
        db.add(client)
        db.commit()
        
        repr_str = repr(client)
        assert "ClientExpeditor" in repr_str
        assert "Dupont" in repr_str

    def test_client_expeditor_email_unique(self, db):
        """Test that email is unique."""
        client1 = ClientExpeditor(
            nom="Dupont",
            prenom="Jean",
            email="jean@example.com",
            telephone="0123456789",
            adresse="123 Rue"
        )
        db.add(client1)
        db.commit()
        
        client2 = ClientExpeditor(
            nom="Martin",
            prenom="Pierre",
            email="jean@example.com",  # Same email
            telephone="0987654321",
            adresse="456 Rue"
        )
        db.add(client2)
        
        with pytest.raises(Exception):
            db.commit()


class TestDestinataireModel:
    """Tests for Destinataire model."""

    def test_destinataire_creation(self, db):
        """Test creating a destinataire."""
        dest = Destinataire(
            nom="Martin",
            prenom="Pierre",
            email="pierre@example.com",
            telephone="0987654321",
            adresse="456 Rue de la Paix"
        )
        db.add(dest)
        db.commit()
        
        assert dest.id is not None
        assert dest.nom == "Martin"

    def test_destinataire_repr(self, db):
        """Test Destinataire __repr__ method."""
        dest = Destinataire(
            nom="Martin",
            prenom="Pierre",
            email="pierre@example.com",
            telephone="0987654321",
            adresse="456 Rue"
        )
        db.add(dest)
        db.commit()
        
        repr_str = repr(dest)
        assert "Destinataire" in repr_str
        assert "Martin" in repr_str


class TestLivreurModel:
    """Tests for Livreur model."""

    def test_livreur_creation(self, db):
        """Test creating a livreur."""
        zone = Zone(nom="Paris", code_postal="75001")
        db.add(zone)
        db.commit()
        
        livreur = Livreur(
            nom="Durand",
            prenom="Marc",
            telephone="0123456789",
            vehicule="Camionnette",
            zone_assignee_id=zone.id
        )
        db.add(livreur)
        db.commit()
        
        assert livreur.id is not None
        assert livreur.nom == "Durand"
        assert livreur.vehicule == "Camionnette"

    def test_livreur_repr(self, db):
        """Test Livreur __repr__ method."""
        zone = Zone(nom="Paris", code_postal="75001")
        db.add(zone)
        db.commit()
        
        livreur = Livreur(
            nom="Durand",
            prenom="Marc",
            telephone="0123456789",
            vehicule="Camionnette",
            zone_assignee_id=zone.id
        )
        db.add(livreur)
        db.commit()
        
        repr_str = repr(livreur)
        assert "Livreur" in repr_str
        assert "Durand" in repr_str


class TestStatutColis:
    """Tests for StatutColis class."""

    def test_statut_colis_constants(self):
        """Test that StatutColis has all required status constants."""
        assert StatutColis.CREE == "cree"
        assert StatutColis.COLLECTE == "collecte"
        assert StatutColis.EN_STOCK == "en_stock"
        assert StatutColis.EN_TRANSIT == "en_transit"
        assert StatutColis.LIVRE == "livre"

    def test_statut_colis_all_statuts(self):
        """Test that ALL_STATUTS contains all statuses."""
        assert len(StatutColis.ALL_STATUTS) == 5
        assert StatutColis.CREE in StatutColis.ALL_STATUTS
        assert StatutColis.COLLECTE in StatutColis.ALL_STATUTS
        assert StatutColis.EN_STOCK in StatutColis.ALL_STATUTS
        assert StatutColis.EN_TRANSIT in StatutColis.ALL_STATUTS
        assert StatutColis.LIVRE in StatutColis.ALL_STATUTS


class TestColisModel:
    """Tests for Colis model."""

    def test_colis_creation(self, db):
        """Test creating a colis."""
        # Create dependencies
        zone = Zone(nom="Paris", code_postal="75001")
        db.add(zone)
        db.commit()
        
        client = ClientExpeditor(
            nom="Dupont",
            prenom="Jean",
            email="jean@example.com",
            telephone="0123456789",
            adresse="123 Rue"
        )
        db.add(client)
        db.commit()
        
        dest = Destinataire(
            nom="Martin",
            prenom="Pierre",
            email="pierre@example.com",
            telephone="0987654321",
            adresse="456 Rue"
        )
        db.add(dest)
        db.commit()
        
        # Create colis
        colis = Colis(
            description="Colis fragile",
            poids=2.5,
            id_client_expeditor=client.id,
            id_destinataire=dest.id,
            id_zone=zone.id,
            ville_destination="Lyon"
        )
        db.add(colis)
        db.commit()
        
        assert colis.id is not None
        assert colis.statut == StatutColis.CREE
        assert colis.poids == 2.5

    def test_colis_repr(self, db):
        """Test Colis __repr__ method."""
        zone = Zone(nom="Paris", code_postal="75001")
        db.add(zone)
        db.commit()
        
        client = ClientExpeditor(
            nom="Dupont",
            prenom="Jean",
            email="jean@example.com",
            telephone="0123456789",
            adresse="123 Rue"
        )
        db.add(client)
        db.commit()
        
        dest = Destinataire(
            nom="Martin",
            prenom="Pierre",
            email="pierre@example.com",
            telephone="0987654321",
            adresse="456 Rue"
        )
        db.add(dest)
        db.commit()
        
        colis = Colis(
            description="Colis fragile",
            poids=2.5,
            id_client_expeditor=client.id,
            id_destinataire=dest.id,
            id_zone=zone.id,
            ville_destination="Lyon"
        )
        db.add(colis)
        db.commit()
        
        repr_str = repr(colis)
        assert "Colis" in repr_str
        assert "fragile" in repr_str


class TestHistoriqueStatutModel:
    """Tests for HistoriqueStatut model."""

    def test_historique_statut_creation(self, db):
        """Test creating historique statut."""
        # Create dependencies
        zone = Zone(nom="Paris", code_postal="75001")
        db.add(zone)
        db.commit()
        
        client = ClientExpeditor(
            nom="Dupont",
            prenom="Jean",
            email="jean@example.com",
            telephone="0123456789",
            adresse="123 Rue"
        )
        db.add(client)
        db.commit()
        
        dest = Destinataire(
            nom="Martin",
            prenom="Pierre",
            email="pierre@example.com",
            telephone="0987654321",
            adresse="456 Rue"
        )
        db.add(dest)
        db.commit()
        
        colis = Colis(
            description="Colis",
            poids=1.0,
            id_client_expeditor=client.id,
            id_destinataire=dest.id,
            id_zone=zone.id,
            ville_destination="Lyon"
        )
        db.add(colis)
        db.commit()
        
        # Create historique
        historique = HistoriqueStatut(
            id_colis=colis.id,
            ancien_statut=StatutColis.CREE,
            nouveau_statut=StatutColis.COLLECTE,
            notes="Colis collecté"
        )
        db.add(historique)
        db.commit()
        
        assert historique.id is not None
        assert historique.ancien_statut == StatutColis.CREE
        assert historique.nouveau_statut == StatutColis.COLLECTE
