import csv, os
from sqlalchemy import create_engine, text

# match your app’s settings
DB_URL = os.getenv('DATABASE_URL', 'sqlite:///data.db')
engine = create_engine(DB_URL)

with engine.connect() as conn, open('full_export.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    result = conn.execute(text("SELECT * FROM invoices"))
    writer.writerow(result.keys())
    writer.writerows(result.fetchall())
print("Exported to full_export.csv")
