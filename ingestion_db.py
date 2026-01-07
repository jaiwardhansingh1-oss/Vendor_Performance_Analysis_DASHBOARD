import pandas as pd
import os 
from sqlalchemy import create_engine
import logging
logging.basicConfig(
    filename="logs/ingestion.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)
engine = create_engine('sqlite:///inventory.db')
import os

print(os.listdir())
begin_inventory = pd.read_csv('begin_inventory.csv')
end_inventory = pd.read_csv('end_inventory.csv')
purchases = pd.read_csv('purchases.csv')
purchase_prices = pd.read_csv('purchase_prices.csv')
sales = pd.read_csv('sales.csv')
vendor_invoice = pd.read_csv('vendor_invoice.csv')

def ingest_db(df, table_name, engine):
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)
    print(f"✅ Inserted: {table_name} ({df.shape[0]} rows)")

# Step 3: List of CSV files
files = [
    'begin_inventory.csv',
    'end_inventory.csv',
    'purchases.csv',
    'purchase_prices.csv',
    'sales.csv',
    'vendor_invoice.csv'
]

def ingest_db(df, table_name,engine):
    df.to_sql(table_name, con = engine , if_exists = 'replace',index= false)
# Step 4: Loop through files
def load_raw_data():
    start = time.time()
    for file in files:
        df = pd.read_csv(file)
        logging.info(f'Ingesting {file} in db')
        ingest_db(df, file[:-4], engine)
        end = time.time()
        total_time = (end - start)/60
        logging.info('Ingestion complete')
        logging.info(f'\ntotal time taken: (total_time) minutes')

if __name__== '__main__':
    load_raw_data()