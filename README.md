# MesaFlow API

Complete REST API for managing restaurant orders, created with **FastAPI**.

The project was designed for a professional Back-End portfolio, simulating a real system used by waiters, kitchen staff, bar staff, and administrators.

## Features

- JWT Authentication
- User and Permission Control
- Table Registration
- People per Table
- Menu with categories and dish images
- Table Order Placement
- Order Notes for Kitchen/Bar
- Separation by Sector: Kitchen or Bar
- Order Status Change
- Preparation Time Estimate
- Payment Control
- Average Ticket Size
- Administrative Dashboard
- Basic Inventory Control
- Low Stock Alerts
- Swagger Automatic Documentation
- Docker Compose with PostgreSQL

## Technologies

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL / SQLite
- JWT
- Pydantic
- Docker
- Pytest

## How to Run Locally with SQLite

```bash python -m venv venv venv\Scripts\activate # Windows pip install -r requirements.txt uvicorn app.main:app --reload

Access:

txt
http://127.0.0.1:8000/docs

## How to run with Docker and PostgreSQL

bash
docker compose up --build


## Initial administrator user

When starting the project, the system automatically creates:

txt
Email: admin@mesaflow.com
Password: admin123

## Structure

txt
mesaflow-api/
├── app/
│ ├── api/routes/
│ ├── core/
│ ├── database/
│ ├── models/
│ ├── schemas/
│ ├── services/
│ └── main.py
├── tests/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md


## Objective

Demonstrate proficiency in creating REST APIs, business rules, authentication, databases, organized architecture, and professional documentation.
