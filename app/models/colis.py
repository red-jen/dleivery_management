from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.connection import Base


class StatutColis:
    CREE = "cree"
    COLLECTE = "collecte"
    EN_STOCK = "en_stock"
    EN_TRANSIT = "en_transit"
    LIVRE = "livre"

    ALL_STATUTS = [CREE, COLLECTE, EN_STOCK, EN_TRANSIT, LIVRE]


class Colis(Base):
    __tablename__ = "colis"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(255), nullable=False)
    poids = Column(Float, nullable=False)  # en kg
    statut = Column(String(50), default=StatutColis.CREE, nullable=False, index=True)
    id_livreur = Column(Integer, ForeignKey("livreurs.id"), nullable=True)
    id_client_expediteur = Column(Integer, ForeignKey("clients_expediteurs.id"), nullable=False)
    id_destinataire = Column(Integer, ForeignKey("destinataires.id"), nullable=False)
    id_zone = Column(Integer, ForeignKey("zones.id"), nullable=False)
    ville_destination = Column(String(100), nullable=False)
    date_creation = Column(DateTime, server_default=func.now(), nullable=False)
    date_modification = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    livreur = relationship("Livreur", back_populates="colis")
    client_expeditor = relationship("ClientExpeditor", back_populates="colis")
    destinataire = relationship("Destinataire", back_populates="colis")
    zone = relationship("Zone", back_populates="colis")
    historique_statuts = relationship("HistoriqueStatut", back_populates="colis", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Colis(id={self.id}, description={self.description}, statut={self.statut}, poids={self.poids})>"
