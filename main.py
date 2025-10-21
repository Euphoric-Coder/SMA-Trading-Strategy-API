from fastapi import FastAPI, HTTPException
from datetime import datetime
from pydantic import BaseModel, condecimal, conint
from prisma import Prisma
import pandas as pd
import uvicorn
from contextlib import asynccontextmanager

db = Prisma()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    yield
    await db.disconnect()


app = FastAPI(title="Simple SMA Trading Strategy API", lifespan=lifespan)


# Pydantic Model for Validation
class StockDataIn(BaseModel):
    datetime: str
    open: condecimal(gt=0)
    high: condecimal(gt=0)
    low: condecimal(gt=0)
    close: condecimal(gt=0)
    volume: conint(gt=0)


# API Endpoints

# GET /data
@app.get("/data")
async def get_all_data():
    """Fetch all stock records."""
    data = await db.stockdata.find_many()
    return {"records": data}


# POST /data
@app.post("/data")
async def add_data(record: StockDataIn):
    """Insert a new record into the database."""
    try:
        new_data = await db.stockdata.create(data=record.model_dump())
        return {"message": "Record added successfully", "record": new_data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# GET /strategy/performance
@app.get("/strategy/performance")
async def strategy_performance(short_window: int = 5, long_window: int = 20):
    """Calculate moving average crossover performance."""
    records = await db.stockdata.find_many(order={"datetime": "asc"})
    if not records or len(records) < long_window:
        raise HTTPException(status_code=400, detail="Not enough data")

    # Convert Prisma model objects to plain dicts
    df = pd.DataFrame(
        [r.model_dump() if hasattr(r, "model_dump") else r for r in records]
    )

    # Ensure the column exists
    if "datetime" not in df.columns:
        raise HTTPException(
            status_code=500,
            detail=f"Missing 'datetime' column. Found: {df.columns.tolist()}",
        )

    # Convert datatypes
    df["datetime"] = pd.to_datetime(df["datetime"])
    df.set_index("datetime", inplace=True)

    # Compute moving averages
    df["short_ma"] = df["close"].astype(float).rolling(window=short_window).mean()
    df["long_ma"] = df["close"].astype(float).rolling(window=long_window).mean()

    # Generate signals
    df["signal"] = 0
    df.loc[df["short_ma"] > df["long_ma"], "signal"] = 1
    df.loc[df["short_ma"] < df["long_ma"], "signal"] = -1

    # Calculate strategy returns
    df["returns"] = df["close"].astype(float).pct_change()
    df["strategy"] = df["signal"].shift(1) * df["returns"]
    performance = (1 + df["strategy"].fillna(0)).prod() - 1

    return {
        "short_window": short_window,
        "long_window": long_window,
        "total_return": round(float(performance * 100), 2),
        "last_signal": int(df["signal"].iloc[-1]),
    }


# Run the app
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
