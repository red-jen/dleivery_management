from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.connection import Base


class HistoriqueStatut(Base):
    __tablename__ = "historique_statuts"

    id = Column(Integer, primary_key=True, index=True)
    id_colis = Column(Integer, ForeignKey("colis.id"), nullable=False, index=True)
    ancien_statut = Column(String(50), nullable=False)
    nouveau_statut = Column(String(50), nullable=False)
    timestamp = Column(DateTime, server_default=func.now(), nullable=False, index=True)
    id_livreur = Column(Integer, ForeignKey("livreurs.id"), nullable=True)
    notes = Column(String(500), nullable=True)

    # Relationships
    colis = relationship("Colis", back_populates="historique_statuts")
    livreur = relationship("Livreur", back_populates="historique_statuts")

    def __repr__(self):
        return f"<HistoriqueStatut(id={self.id}, id_colis={self.id_colis}, ancien_statut={self.ancien_statut}, nouveau_statut={self.nouveau_statut})>"
