# Simple SMA Trading Strategy API (FastAPI + Prisma + PostgreSQL)

This project implements a **Moving Average Crossover Trading Strategy** backend using **FastAPI**, **Prisma ORM**, and **PostgreSQL**.  
It provides endpoints to **insert**, **retrieve**, and **analyze stock market data**, supporting real-world use cases for algorithmic trading and quantitative analysis.

---

## Features

- **FastAPI-based RESTful API** with async endpoints  
- **Prisma ORM** integration for PostgreSQL database access  
- **Moving Average Crossover Strategy** for trading signal generation  
- **Pydantic-based input validation** for clean, reliable data  
- **Unit tests with >90% coverage** (using `unittest` + `coverage`)  
- **Container-ready architecture** (easily deployable via Docker)  

---

## Project Structure
```txt
./
├── prisma/
│   └── schema.prisma (Prisma Schema for defining the StockData model)
├── insert_data.py (To Load the CSV data into the database)
├── main.py (For FASTAPI application with endpoints)
├── test_app.py (For Unit Tests for validation and the strategic logic)
└── requirements.txt
```

---


## Endpoints Overview

### 1. **POST `/data`**
Insert a single record into the database.

#### Screenshot of Browser:
![Alt text](path/to/image.jpg "Optional Title")

#### Example Request:
```json
{
  "datetime": "2025-01-01T09:15:00",
  "open": 100.5,
  "high": 102.0,
  "low": 99.8,
  "close": 101.2,
  "volume": 15342
}
```

#### Example Response:
```json
{
  "message": "Record added successfully",
  "record": {
    "id": 1,
    "datetime": "2025-01-01T09:15:00",
    "open": 100.5,
    "high": 102.0,
    "low": 99.8,
    "close": 101.2,
    "volume": 15342
  }
}
```
