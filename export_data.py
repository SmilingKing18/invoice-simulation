import csv, os
from sqlalchemy import create_engine, text

DB_URL = os.getenv('DATABASE_URL', 'sqlite:///data.db')
engine = create_engine(DB_URL)

with engine.connect() as conn:
    # Invoices
    with open('invoices.csv','w',newline='') as f:
        writer=csv.writer(f)
        result = conn.execute(text("SELECT * FROM invoices"))
        writer.writerow(result.keys())
        writer.writerows(result.fetchall())

    # Demographics
    with open('demographics.csv','w',newline='') as f:
        writer=csv.writer(f)
        result = conn.execute(text("SELECT * FROM demographics"))
        writer.writerow(result.keys())
        writer.writerows(result.fetchall())

print("Exports complete: invoices.csv + demographics.csv")
