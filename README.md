# SMA Trading Strategy API (FastAPI + Prisma + PostgreSQL)

This project implements a **Moving Average Crossover Trading Strategy** backend using **FastAPI**, **Prisma ORM**, and **PostgreSQL (NeonDB)**.  
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
.
├── prisma/
│   └── schema.prisma
├── screenshots/
│   └── all-screenshots
├── Dockerfile
├── insert_data.py
├── main.py
├── requirements.txt
├── stock_data.csv
└── test_app.py
```

---

### **Setting Up a Virtual Environment**

Before installing dependencies or running the project, it’s recommended to create and activate a **virtual environment**.

---

#### **Create a Virtual Environment**

Run the following command in your project’s root directory:

```bash
python -m venv VIRTUAL
```

---

### **Project Setup & Initialization Commands**

Follow these steps to correctly set up and run the FastAPI + Prisma + PostgreSQL trading strategy assignment.

---

#### **Install Required Dependencies**

Once you have cloned or downloaded the project, install all the dependencies from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

#### **Generate Prisma Client**
```bash
prisma generate
```

##### Screenshot of the Prisma Client Generation Terminal:
![PRISMA GENERATE](/screenshots/PRISMA%20GENERATE.png "Optional Title")

#### **Push Schema to Database**
```bash
prisma db push
```

##### Screenshot of the Prisma Schema Pushed to DB on NeonDB (PostgreSQL):
![PRISMA PUSH](/screenshots/PRISMA%20PUSH.png "Optional Title")

#### **Insert the Dataset**

Download the stock data manually from the given Google Sheets link:  
> [Stock Data Spreadsheet](https://docs.google.com/spreadsheets/d/1-rIkEb94tZ69FvsjXnfkVETYu6rftF-8/edit?rtpof=true)

Save it locally in your project directory as:
`stock_data.csv`

Then, run the following command to insert all CSV data into the database:
```bash
python insert_data.py
```

##### Screenshot of Data Insertion on the DB:
![DATA INSERTION](/screenshots/DATA%20INSERTION.png "Optional Title")

---

## Endpoints Overview

### 1. **GET `/data`**
Shows all data from the database

#### Screenshot of the Browser (Begin):
![GET /data begin](/screenshots/GET%20:data%20API%20Result%201st.png "Optional Title")

#### Screenshot of the Browser (End):
![GET /data end](/screenshots/GET%20:data%20API%20Result%20Last.png "Optional Title")

### 2. **POST `/data`**
Insert a single record into the database.

#### Screenshot of Terminal Command:
![POST /data terminal](/screenshots/POST%20:data%20API%20Result.png "Optional Title")

#### Screenshot of Browser Result after adding data:
![POST /data screenshot](/screenshots/POST%20:data%20Proof.png "Optional Title")

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

### 3. **GET `/strategy/performance`**
Calculates the Moving Average Crossover strategy using the stored data.

### **Query Parameters**

| Parameter | Type | Default | Description |
|------------|------|----------|--------------|
| **`short_window`** | `integer` | `5` | The number of periods used to calculate the **short-term moving average**. |
| **`long_window`** | `integer` | `20` | The number of periods used to calculate the **long-term moving average**. |


#### Screenshot of the Result:
![GET /strategy/performance screenshot](/screenshots/GET%20%20:strategy:performance%20API%20Result.png "Optional Title")

### **Dockerfile Overview**

This project includes a **Dockerfile** for containerizing the FastAPI application, ensuring consistent deployment across environments.

#### **Key Steps in Dockerfile**

| Stage | Description |
|--------|--------------|
| **Base Image** | Uses `python:3.10-slim` for a lightweight environment. |
| **Environment Variables** | Sets `PYTHONDONTWRITEBYTECODE=1` and `PYTHONUNBUFFERED=1` to prevent `.pyc` files and enable real-time logs. |
| **Dependencies** | Installs system tools (`build-essential`, `libpq-dev`, etc.) and Python dependencies from `requirements.txt`. |
| **Prisma Setup** | Installs Prisma CLI and generates the Python Prisma client (`prisma generate`). |
| **Expose Port** | Opens port `8000` for the FastAPI app. |
| **Run Command** | Starts the app using `uvicorn main:app --host 0.0.0.0 --port 8000`. |

#### **Build & Run Commands**

```bash
docker build -t invsto-sma-trading-strategy-api .
```

```bash
docker run -p 8000:8000 invsto-sma-trading-strategy-api
```

### **Unit Testing Overview**

Unit testing is an essential part of this project to ensure all API endpoints, data validations, and trading strategy calculations work correctly and reliably and everything is functionally correct.

---

#### **Purpose of Unit Tests**

The test is written using Python’s built-in `unittest` framework and focus on the following:

| Test Category | Description |
|----------------|--------------|
| **Input Validation** | Ensures `/data` endpoint rejects invalid inputs (e.g., negative prices, non-numeric volume). |
| **Data Insertion** | Verifies that valid records are successfully stored in the PostgreSQL database. |
| **Strategy Logic** | Checks that the **Moving Average Crossover Strategy** computes signals and returns accurately. |
| **Error Handling** | Confirms that the API gracefully handles missing data or insufficient records for calculations. |
| **API Structure** | Tests endpoint responses to confirm expected JSON structure and HTTP status codes. |

---

#### **How to Run the Tests**

Run all tests and view a coverage report with:

```bash
coverage run -m unittest discover -s . -p "test*.py"
coverage report -m
```

#### Screenshot of the Unit Testing results:
![Unit Test Results](/screenshots/UNIT%20TEST%20RESULT.png "Optional Title")