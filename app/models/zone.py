from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.connection import Base


class Zone(Base):
    __tablename__ = "zones"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100), nullable=False, unique=True)
    code_postal = Column(String(20), nullable=False, unique=True)

    # Relationships
    colis = relationship("Colis", back_populates="zone")
    livreurs = relationship("Livreur", back_populates="zone")

    def __repr__(self):
        return f"<Zone(id={self.id}, nom={self.nom}, code_postal={self.code_postal})>"
