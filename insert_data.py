import asyncio
import csv
from datetime import datetime
from decimal import Decimal
from prisma import Prisma
from dotenv import load_dotenv

# Load .env for DATABASE_URL
load_dotenv()

CSV_PATH = "stock_data.csv" 


async def main():
    print(f"Reading data from '{CSV_PATH}'...")
    db = Prisma()
    await db.connect()

    valid_rows = []
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                # Skip rows if missing required fields
                if not row.get("datetime") or not row.get("close"):
                    continue

                # Convert types carefully
                record = {
                    "datetime": datetime.fromisoformat(
                        row["datetime"].replace("Z", "").strip()
                    ),
                    "open": Decimal(str(row["open"]).strip()),
                    "high": Decimal(str(row["high"]).strip()),
                    "low": Decimal(str(row["low"]).strip()),
                    "close": Decimal(str(row["close"]).strip()),
                    "volume": int(float(row["volume"])),
                }

                valid_rows.append(record)
            except Exception as e:
                print(f"Skipping invalid row: {row} -> {e}")

    print(f"{len(valid_rows)} valid rows ready for insertion.")

    # Clear old records before inserting new data
    await db.stockdata.delete_many()
    print("Cleared existing data.")

    if not valid_rows:
        print("No valid rows found. Please check the CSV format.")
        await db.disconnect()
        return

    # Insert in chunks
    CHUNK_SIZE = 500
    inserted = 0
    for i in range(0, len(valid_rows), CHUNK_SIZE):
        chunk = valid_rows[i : i + CHUNK_SIZE]
        await db.stockdata.create_many(data=chunk, skip_duplicates=True)
        inserted += len(chunk)
        print(f"Inserted {inserted}/{len(valid_rows)} rows...")

    await db.disconnect()
    print("All data inserted successfully!")


if __name__ == "__main__":
    asyncio.run(main())
