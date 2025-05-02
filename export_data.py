import csv, os
from sqlalchemy import create_engine, text
load_dotenv = __import__('dotenv').load_dotenv
load_dotenv()
DB_URL = os.getenv('DATABASE_URL','sqlite:///data.db')
engine = create_engine(DB_URL)

with engine.connect() as conn:
    for name, query in [
      ('invoices.csv', 'SELECT * FROM invoices'),
      ('demographics.csv', 'SELECT * FROM demographics'),
    ]:
        with open(name,'w',newline='') as f:
            writer=csv.writer(f)
            result=conn.execute(text(query))
            writer.writerow(result.keys())
            writer.writerows(result.fetchall())
print('Exported CSVs')