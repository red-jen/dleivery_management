# YouExpress - Delivery Management System

FastAPI-based delivery management application for Morocco.

## Tech Stack

- FastAPI 0.104.1
- SQLAlchemy 2.0.23
- PostgreSQL / SQLite
- Pydantic 2.5.0
- pytest 7.4.3

## Setup

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pytest tests/ -v
python main.py
```

## API Docs

- Swagger: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

`
delivery/
 app/
    models/         # SQLAlchemy models
    routes/         # FastAPI routes
    schemas/        # Pydantic schemas
    database/       # DB config
    config.py       # Settings
    main.py         # App init
 tests/              # Unit & integration tests
 main.py             # Entry point
 requirements.txt    # Dependencies
`

## API Endpoints

### Zones
- POST /api/v1/zones/ - Create zone
- GET /api/v1/zones/ - List zones
- GET /api/v1/zones/{id} - Get zone
- PUT /api/v1/zones/{id} - Update zone
- DELETE /api/v1/zones/{id} - Delete zone

### Health
- GET /health - Health check
- GET / - Root endpoint

## Testing

`ash
pytest tests/ -v
`

Coverage: 93% (39/42 tests passing)
