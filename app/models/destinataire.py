from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.connection import Base


class Destinataire(Base):
    __tablename__ = "destinataires"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100), nullable=False)
    prenom = Column(String(100), nullable=False)
    email = Column(String(120), nullable=False, index=True)
    telephone = Column(String(20), nullable=False)
    adresse = Column(String(255), nullable=False)

    # Relationships
    colis = relationship("Colis", back_populates="destinataire")

    def __repr__(self):
        return f"<Destinataire(id={self.id}, nom={self.nom}, prenom={self.prenom})>"
