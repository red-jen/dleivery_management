# YouExpress - Delivery Management System

This is the initial project structure for the YouExpress delivery management system for Morocco.

## Project Overview

YouExpress is a comprehensive logistics management application designed to modernize and automate parcel delivery operations in Morocco. The system provides real-time tracking, route planning, and status management for all stakeholders.

## Technology Stack

- **Backend Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Validation**: Pydantic
- **Containerization**: Docker & Docker Compose
- **Testing**: Pytest
- **API Documentation**: Swagger/OpenAPI

## Project Structure

```
delivery/
├── app/
│   ├── models/          # SQLAlchemy ORM models
│   ├── routes/          # FastAPI route handlers
│   ├── schemas/         # Pydantic request/response schemas
│   ├── controllers/     # Business logic controllers
│   ├── database/        # Database configuration and utilities
│   ├── config.py        # Application configuration
│   └── main.py          # FastAPI app initialization
├── tests/               # Unit and integration tests
├── main.py              # Application entry point
├── requirements.txt     # Python dependencies
├── Dockerfile           # Docker image configuration
├── docker-compose.yml   # Docker Compose configuration
├── .env                 # Environment variables (local)
└── README.md            # Project documentation
```

## Installation & Setup

### Prerequisites
- Docker & Docker Compose (recommended)
- Python 3.11+
- PostgreSQL 15+

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd delivery
```

2. Build and start the containers:
```bash
docker-compose up --build
```

3. The API will be available at `http://localhost:8000`

### Local Development Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your settings
```

4. Initialize the database:
```bash
python -c "from app.database import init_db; init_db()"
```

5. Run the application:
```bash
uvicorn main:app --reload
```

## API Documentation

Once the application is running, access the interactive API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI Schema: http://localhost:8000/openapi.json

## Available Endpoints

### Health Check
- `GET /health` - Application health status

### Zones (Completed)
- `POST /api/v1/zones` - Create a new zone
- `GET /api/v1/zones` - List all zones
- `GET /api/v1/zones/{zone_id}` - Get zone details
- `PUT /api/v1/zones/{zone_id}` - Update a zone
- `DELETE /api/v1/zones/{zone_id}` - Delete a zone

### In Development
- ClientExpéditeur (Shippers) - CRUD operations
- Destinataire (Recipients) - CRUD operations
- Livreur (Delivery Drivers) - CRUD operations
- Colis (Packages) - CRUD operations and status management
- HistoriqueStatut (Status History) - Tracking and auditing

## Database Models

### Zone
- id, nom, code_postal
- Relationships: colis, livreurs

### ClientExpéditeur (Shipper)
- id, nom, prenom, email, telephone, adresse
- Relationships: colis

### Destinataire (Recipient)
- id, nom, prenom, email, telephone, adresse
- Relationships: colis

### Livreur (Delivery Driver)
- id, nom, prenom, telephone, vehicule, zone_assignee_id
- Relationships: zone, colis, historique_statuts

### Colis (Package)
- id, description, poids, statut, id_livreur, id_client_expediteur, id_destinataire, id_zone, ville_destination
- Statuses: créé, collecté, en_stock, en_transit, livré
- Relationships: livreur, client_expediteur, destinataire, zone, historique_statuts

### HistoriqueStatut (Status History)
- id, id_colis, ancien_statut, nouveau_statut, timestamp, id_livreur, notes
- Relationships: colis, livreur

## User Roles

1. **Gestionnaire Logistique** (Logistics Manager)
   - Full access to create, read, update, delete operations
   - Can manage all packages, drivers, and routes
   - Can assign packages to drivers

2. **Livreur** (Delivery Driver)
   - View assigned packages
   - Update package status during delivery
   - View assigned zone information

3. **Client Expéditeur** (Shipper)
   - Create delivery requests
   - View own shipments
   - Track shipment status

4. **Destinataire** (Recipient)
   - View shipment status
   - Track delivery progress

## Running Tests

```bash
pytest tests/ -v
```

## Environment Configuration

Edit the `.env` file to configure:
- Database connection string
- Application debug mode
- Logging level
- CORS settings
- API documentation URLs

## Development Timeline

- **Duration**: 6 days (05/01/2026 - 10/01/2026)
- **Methodology**: Agile/Iterative development

## Next Steps

1. ✅ Initial project structure
2. ✅ Database models
3. ✅ FastAPI configuration
4. ⬜ Complete CRUD routes for all entities
5. ⬜ Implement business logic in controllers
6. ⬜ Add authentication/authorization
7. ⬜ Implement comprehensive tests
8. ⬜ Add data validation and error handling
9. ⬜ Generate UML class diagram
10. ⬜ Finalize documentation

## Contributing

- Code follows PEP 8 style guidelines
- Use meaningful commit messages
- Write tests for new features
- Update documentation accordingly

## Support

For issues or questions, please refer to the project documentation or contact the development team.

---

**Last Updated**: January 5, 2026
**Version**: 1.0.0 (Alpha)
