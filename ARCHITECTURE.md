# YouExpress System Architecture & Database Schema

## 🏗️ System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT APPLICATIONS                       │
│         (Web UI, Mobile App, Admin Dashboard)                    │
└──────────────┬──────────────────────────────────────────────────┘
               │ HTTP REST Requests
               ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API GATEWAY LAYER                           │
│                    (FastAPI Application)                         │
├─────────────────────────────────────────────────────────────────┤
│  GET/POST/PUT/DELETE /api/v1/*                                  │
│  - Health checks                                                 │
│  - CORS handling                                                 │
│  - Exception handling                                            │
│  - Request validation                                            │
└──────────────┬──────────────────────────────────────────────────┘
               │
┌──────────────▼──────────────────────────────────────────────────┐
│                    APPLICATION LAYERS                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌───────────────────────────────────────────────────────┐      │
│  │  ROUTES LAYER (app/routes/)                           │      │
│  │  ├── zones.py              ← Fully implemented        │      │
│  │  ├── clients.py            ← To implement             │      │
│  │  ├── destinataires.py      ← To implement             │      │
│  │  ├── livreurs.py           ← To implement             │      │
│  │  └── colis.py              ← To implement             │      │
│  │  Responsibilities:                                     │      │
│  │  • Handle HTTP requests/responses                     │      │
│  │  • Validate input (Pydantic schemas)                  │      │
│  │  • Call business logic                                │      │
│  │  • Return formatted responses                         │      │
│  └───────────────────────────────────────────────────────┘      │
│                          ▲                                       │
│                          │ Calls                                 │
│                          ▼                                       │
│  ┌───────────────────────────────────────────────────────┐      │
│  │  CONTROLLERS LAYER (app/controllers/)                 │      │
│  │  ├── zone_controller.py    ← To implement             │      │
│  │  ├── client_controller.py   ← To implement            │      │
│  │  ├── colis_controller.py    ← To implement            │      │
│  │  └── ...                                              │      │
│  │  Responsibilities:                                     │      │
│  │  • Implement business logic                           │      │
│  │  • Data processing & transformation                   │      │
│  │  • Complex operations                                 │      │
│  │  • Validation rules                                   │      │
│  └───────────────────────────────────────────────────────┘      │
│                          ▲                                       │
│                          │ Uses                                  │
│                          ▼                                       │
│  ┌───────────────────────────────────────────────────────┐      │
│  │  MODELS LAYER (app/models/)                           │      │
│  │  ├── zone.py               ← Fully implemented        │      │
│  │  ├── client_expediteur.py  ← Fully implemented        │      │
│  │  ├── destinataire.py       ← Fully implemented        │      │
│  │  ├── livreur.py            ← Fully implemented        │      │
│  │  ├── colis.py              ← Fully implemented        │      │
│  │  └── historique_statut.py  ← Fully implemented        │      │
│  │  Responsibilities:                                     │      │
│  │  • Define database tables                             │      │
│  │  • Define relationships                               │      │
│  │  • ORM mapping                                        │      │
│  └───────────────────────────────────────────────────────┘      │
│                          ▲                                       │
│                          │ CRUD                                  │
│                          ▼                                       │
└──────────────┬──────────────────────────────────────────────────┘
               │
┌──────────────▼──────────────────────────────────────────────────┐
│                      DATA ACCESS LAYER                           │
│         (SQLAlchemy ORM + Database Connection)                  │
└──────────────┬──────────────────────────────────────────────────┘
               │
┌──────────────▼──────────────────────────────────────────────────┐
│                    DATABASE LAYER                                │
│            (PostgreSQL - Docker Container)                       │
├─────────────────────────────────────────────────────────────────┤
│  ├── zones table                                                │
│  ├── clients_expediteurs table                                  │
│  ├── destinataires table                                        │
│  ├── livreurs table                                             │
│  ├── colis table                                                │
│  └── historique_statuts table                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📊 DATABASE SCHEMA - Entity Relationship Diagram

```
┌──────────────────────┐                    ┌──────────────────────┐
│       ZONE           │                    │    CLIENT_EXPEDITEUR │
├──────────────────────┤                    ├──────────────────────┤
│ id (PK)              │                    │ id (PK)              │
│ nom                  │                    │ nom                  │
│ code_postal (UNIQUE) │                    │ prenom               │
│                      │                    │ email (UNIQUE)       │
│                      │                    │ telephone            │
│                      │                    │ adresse              │
└──────┬───────────────┘                    └────────┬─────────────┘
       │                                             │
       │ 1 ─── N                                    │ 1 ─── N
       │                                             │
       │                                             │
   ┌───┴─────────────────────────────────────────────┴────────┐
   │                                                            │
   │                     COLIS (Package)                       │
   │                 ┌──────────────────────┐                 │
   │                 │ id (PK)              │                 │
   │                 │ description          │                 │
   │                 │ poids                │                 │
   │                 │ statut               │                 │
   │                 │ id_client (FK)   ────┼──→ CLIENT_EXPEDITEUR
   │                 │ id_destinataire (FK)─┼──→ DESTINATAIRE
   │                 │ id_livreur (FK)  ────┼──→ LIVREUR
   │                 │ id_zone (FK)     ────┼──→ ZONE
   │                 │ ville_destination    │
   │                 │ date_creation        │
   │                 │ date_modification    │
   │                 └──────────────────────┘
   │                          │
   │                          │ 1 ─── N
   │                          │
   │                 ┌────────┴───────┐
   │                 │                │
   │  ┌──────────────────────┐  ┌─────────────────────┐
   │  │ DESTINATAIRE         │  │ LIVREUR             │
   │  ├──────────────────────┤  ├─────────────────────┤
   │  │ id (PK)              │  │ id (PK)             │
   │  │ nom                  │  │ nom                 │
   │  │ prenom               │  │ prenom              │
   │  │ email (UNIQUE)       │  │ telephone           │
   │  │ telephone            │  │ vehicule            │
   │  │ adresse              │  │ zone_assignee_id(FK)│
   │  └──────────────────────┘  └────────┬────────────┘
   │                                      │
   │                                      └─→ ZONE
   │
   └─→ HISTORIQUE_STATUT
       ┌──────────────────────┐
       │ id (PK)              │
       │ id_colis (FK)    ────┼──→ COLIS
       │ ancien_statut        │
       │ nouveau_statut       │
       │ timestamp            │
       │ id_livreur (FK)  ────┼──→ LIVREUR
       │ notes                │
       └──────────────────────┘
```

---

## 📈 Data Flow Example: Creating a Delivery

```
┌─ CLIENT APPLICATION ─┐
│ POST /api/v1/colis   │
│ {                    │
│   description: "...",│
│   poids: 5,          │
│   ...                │
│ }                    │
└──────────┬───────────┘
           │
           ▼
┌─────────────────────────┐
│ ROUTE: colis.py         │
│ ├─ Validate (Pydantic)  │
│ ├─ Check permissions    │
│ └─ Call controller      │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│ CONTROLLER              │
│ ├─ Apply business logic │
│ ├─ Check constraints    │
│ ├─ Create record        │
│ └─ Log operation        │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│ DATABASE OPERATION      │
│ INSERT INTO colis (     │
│   description, poids... │
│ )                       │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│ Response to Client      │
│ 201 Created             │
│ {                       │
│   id: 1,                │
│   statut: "créé",       │
│   ...                   │
│ }                       │
└─────────────────────────┘
```

---

## 🔄 Package Lifecycle

```
┌──────────┐
│  CRÉÉ    │  ← Package created in system
└─────┬────┘
      │ Collection scheduled
      ▼
┌──────────────┐
│  COLLECTÉ    │  ← Picked up from sender
└─────┬────────┘
      │ Transported to warehouse
      ▼
┌──────────────┐
│   EN_STOCK   │  ← Stored in warehouse
└─────┬────────┘
      │ Assigned to driver & loaded
      ▼
┌──────────────┐
│  EN_TRANSIT  │  ← On delivery route
└─────┬────────┘
      │ Delivered to recipient
      ▼
┌──────────────┐
│   LIVRÉ      │  ← Delivery complete
└──────────────┘

Each status change is logged in HISTORIQUE_STATUT table
```

---

## 🔗 Route Structure Organization

```
/api/v1/
├── /zones
│   ├── POST   / (create)
│   ├── GET    / (list all)
│   ├── GET    /{id} (get one)
│   ├── PUT    /{id} (update)
│   └── DELETE /{id} (delete)
│
├── /clients
│   ├── POST   / (create)
│   ├── GET    / (list)
│   ├── GET    /{id} (get one)
│   ├── PUT    /{id} (update)
│   └── DELETE /{id} (delete)
│
├── /destinataires
│   └── ... (same pattern)
│
├── /livreurs
│   └── ... (same pattern)
│
├── /colis
│   ├── POST   / (create)
│   ├── GET    / (list, with filters)
│   ├── GET    /{id} (get one)
│   ├── PUT    /{id} (update)
│   ├── DELETE /{id} (delete)
│   ├── PUT    /{id}/statut (change status)
│   └── GET    /{id}/historique (view history)
│
└── /historique
    ├── GET    / (list all)
    └── GET    /?id_colis={id} (filter by colis)
```

---

## 👥 User Access Control (To Implement Phase 4)

```
┌──────────────────────────────────────────────────────┐
│          GESTIONNAIRE LOGISTIQUE                      │
│          (Logistics Manager)                          │
│  ✓ Full CRUD on all entities                         │
│  ✓ Assign packages to drivers                        │
│  ✓ View all statistics                               │
└──────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────┐
│          LIVREUR (Driver)                             │
│  ✓ View own assigned packages                        │
│  ✓ Update delivery status                            │
│  ✓ View own zone information                         │
│  ✗ Cannot create/delete packages                     │
│  ✗ Cannot access other drivers' deliveries           │
└──────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────┐
│          CLIENT EXPÉDITEUR (Shipper)                  │
│  ✓ Create delivery requests (Colis)                  │
│  ✓ View own shipments                                │
│  ✓ Track shipment status                             │
│  ✗ Cannot delete others' packages                    │
│  ✗ Cannot assign to drivers                          │
└──────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────┐
│          DESTINATAIRE (Recipient)                     │
│  ✓ View own deliveries                               │
│  ✓ Track delivery status                             │
│  ✗ Cannot create/modify packages                     │
│  ✗ Cannot see other recipients' packages             │
└──────────────────────────────────────────────────────┘
```

---

## 📋 SQL Table Details

### ZONES
```sql
CREATE TABLE zones (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL UNIQUE,
    code_postal VARCHAR(20) NOT NULL UNIQUE
);
```

### CLIENTS_EXPEDITEURS
```sql
CREATE TABLE clients_expediteurs (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    telephone VARCHAR(20) NOT NULL,
    adresse VARCHAR(255) NOT NULL
);
```

### DESTINATAIRES
```sql
CREATE TABLE destinataires (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL,
    telephone VARCHAR(20) NOT NULL,
    adresse VARCHAR(255) NOT NULL
);
```

### LIVREURS
```sql
CREATE TABLE livreurs (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    telephone VARCHAR(20) NOT NULL,
    vehicule VARCHAR(100) NOT NULL,
    zone_assignee_id INTEGER NOT NULL REFERENCES zones(id)
);
```

### COLIS
```sql
CREATE TABLE colis (
    id SERIAL PRIMARY KEY,
    description VARCHAR(255) NOT NULL,
    poids FLOAT NOT NULL,
    statut VARCHAR(50) DEFAULT 'créé',
    id_livreur INTEGER REFERENCES livreurs(id),
    id_client_expediteur INTEGER NOT NULL REFERENCES clients_expediteurs(id),
    id_destinataire INTEGER NOT NULL REFERENCES destinataires(id),
    id_zone INTEGER NOT NULL REFERENCES zones(id),
    ville_destination VARCHAR(100) NOT NULL,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### HISTORIQUE_STATUTS
```sql
CREATE TABLE historique_statuts (
    id SERIAL PRIMARY KEY,
    id_colis INTEGER NOT NULL REFERENCES colis(id),
    ancien_statut VARCHAR(50) NOT NULL,
    nouveau_statut VARCHAR(50) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_livreur INTEGER REFERENCES livreurs(id),
    notes VARCHAR(500)
);
```

---

**Architecture Design**: January 5, 2026  
**Version**: 1.0  
**Team**: YouExpress Development
