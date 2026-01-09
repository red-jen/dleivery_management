from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.connection import Base


class Livreur(Base):
    __tablename__ = "livreurs"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100), nullable=False)
    prenom = Column(String(100), nullable=False)
    telephone = Column(String(20), nullable=False)
    vehicule = Column(String(100), nullable=False)
    zone_assignee_id = Column(Integer, ForeignKey("zones.id"), nullable=False)

    # Relationships
    zone = relationship("Zone", back_populates="livreurs")
    colis = relationship("Colis", back_populates="livreur")
    historique_statuts = relationship("HistoriqueStatut", back_populates="livreur")

    def __repr__(self):
        return f"<Livreur(id={self.id}, nom={self.nom}, prenom={self.prenom}, vehicule={self.vehicule})>"
