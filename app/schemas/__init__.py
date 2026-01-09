from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# Zone Schemas
class ZoneBase(BaseModel):
    nom: str = Field(..., min_length=1, max_length=100)
    code_postal: str = Field(..., min_length=1, max_length=20)


class ZoneCreate(ZoneBase):
    pass


class ZoneUpdate(BaseModel):
    nom: Optional[str] = None
    code_postal: Optional[str] = None


class Zone(ZoneBase):
    id: int

    class Config:
        from_attributes = True


# ClientExpeditor Schemas
class ClientExpeditorBase(BaseModel):
    nom: str = Field(..., min_length=1, max_length=100)
    prenom: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    telephone: str = Field(..., min_length=10, max_length=20)
    adresse: str = Field(..., min_length=1, max_length=255)


class ClientExpeditorCreate(ClientExpeditorBase):
    pass


class ClientExpeditorUpdate(BaseModel):
    nom: Optional[str] = None
    prenom: Optional[str] = None
    email: Optional[EmailStr] = None
    telephone: Optional[str] = None
    adresse: Optional[str] = None


class ClientExpeditor(ClientExpeditorBase):
    id: int

    class Config:
        from_attributes = True


# Destinataire Schemas
class DestinataireBase(BaseModel):
    nom: str = Field(..., min_length=1, max_length=100)
    prenom: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    telephone: str = Field(..., min_length=10, max_length=20)
    adresse: str = Field(..., min_length=1, max_length=255)


class DestinataireCreate(DestinataireBase):
    pass


class DestinataireUpdate(BaseModel):
    nom: Optional[str] = None
    prenom: Optional[str] = None
    email: Optional[EmailStr] = None
    telephone: Optional[str] = None
    adresse: Optional[str] = None


class Destinataire(DestinataireBase):
    id: int

    class Config:
        from_attributes = True


# Livreur Schemas
class LivreurBase(BaseModel):
    nom: str = Field(..., min_length=1, max_length=100)
    prenom: str = Field(..., min_length=1, max_length=100)
    telephone: str = Field(..., min_length=10, max_length=20)
    vehicule: str = Field(..., min_length=1, max_length=100)
    zone_assignee_id: int


class LivreurCreate(LivreurBase):
    pass


class LivreurUpdate(BaseModel):
    nom: Optional[str] = None
    prenom: Optional[str] = None
    telephone: Optional[str] = None
    vehicule: Optional[str] = None
    zone_assignee_id: Optional[int] = None


class Livreur(LivreurBase):
    id: int

    class Config:
        from_attributes = True


# Colis Schemas
class ColisBase(BaseModel):
    description: str = Field(..., min_length=1, max_length=255)
    poids: float = Field(..., gt=0)
    id_client_expediteur: int
    id_destinataire: int
    id_zone: int
    ville_destination: str = Field(..., min_length=1, max_length=100)


class ColisCreate(ColisBase):
    pass


class ColisUpdate(BaseModel):
    description: Optional[str] = None
    poids: Optional[float] = None
    id_client_expediteur: Optional[int] = None
    id_destinataire: Optional[int] = None
    id_zone: Optional[int] = None
    id_livreur: Optional[int] = None
    ville_destination: Optional[str] = None


class ColisStatusUpdate(BaseModel):
    statut: str = Field(..., min_length=1)
    notes: Optional[str] = None


class Colis(ColisBase):
    id: int
    statut: str
    id_livreur: Optional[int]
    date_creation: datetime
    date_modification: datetime

    class Config:
        from_attributes = True


# HistoriqueStatut Schemas
class HistoriqueStatutBase(BaseModel):
    id_colis: int
    ancien_statut: str
    nouveau_statut: str


class HistoriqueStatutCreate(HistoriqueStatutBase):
    id_livreur: Optional[int] = None
    notes: Optional[str] = None


class HistoriqueStatut(HistoriqueStatutBase):
    id: int
    timestamp: datetime
    id_livreur: Optional[int]
    notes: Optional[str]

    class Config:
        from_attributes = True
