import sqlite3
import pandas as pd
import logging
import ingestion_db import ingest

logging.basicconfig(
    filename ="log/get_vendor_summary.log",
    level = logging.DEBUG,
    format = %(asctime)s - %(levelname)s - %(message)s",
filemode="a"
) 
 
def create_vendor_summary(conn):
    ''' this function will merde the different table to get the overall vendor summary and adding new columns in the resultant data'''
    vendor_sales_summary = pd.read_sql_query("""WITH Freight Summary AS (
    SELECT
         VendorNumber,
    SUM(Freight) AS FreightCost
    FROM vendor_invoice
    GROUP BY VendoNumber
    ),

    PurchaseSummary AS (
    SELECT
        p.VendorNumber,
        p.VendorName,
        p.Brand,
        p.Description,
        p.PurchasePrice,
        pp.Volume,
        SUM(p.Quantity) AS TotalPurchaseQuantity,
        SUM(p.Dollars) AS TotalPurchaseDollars
    FROM purchases p
    JOIN purchase_prices pp
        ON p.Brand = pp.Brand 
    WHERE p.PurchasePrice > 0
    GROUP BY p.VendorNumber, p.VendorName, p.Brand, p.Description, p.PurchasePrice, pp.Volume
),

    SalesSummary AS (
    SELECT
        VendorNo,
        Brand,
        SUM(SalesDollars) AS TotalSalesDollars,
        SUM(SalesPrice) AS TotalSalesPrice,
        SUM(SalesQuantity) AS TotalSalesQuantity,
        SUM(ExciseTax) AS TotalExciseTax
    FROM sales
    GROUP BY VendorNo, Brand
)

    SELECT
    ps.VendorNumber,
    ps.VendorName,
    ps.Brand,
    ps.Description,
    ps.PurchasePrice,
    ps.Volume,
    ps.TotalPurchaseQuantity,
    ps.TotalPurchaseDollars,
    ss.TotalSalesDollars,
    ss.TotalSalesPrice,
    ss.TotalSalesQuantity,
    ss.TotalExciseTax,
    fs.FreightCost
FROM PurchaseSummary ps
LEFT JOIN SalesSummary ss
    ON ps.VendorNumber = ss.VendorNo
    AND ps.Brand = ss.Brand
LEFT JOIN FreightSummary fs
    ON ps.VendorNumber = fs.VendorNumber
ORDER BY ps.TotalPurchaseDollars DESC
""", conn)

return vendor_sales_summary


def clean_data(df):
    '''this function will clear the data'''
    # changing datatype to float
    df['Volume'] = df['Volume'].astype('float')

    # filling missing value with 0
    df.fillna(0, inplace = True)

    # removing spaces from categorical columns
    df['VendorName'] = df['VendorName'].str.strip()
    df['Description'] = df['Description'].str.strip()

   # ceating new columns for better analysis
     vendor_sales_summary['GrossProfit'] = vendor_sales_summary['TotalSalesDollars'] - vendor_sales_summary['TotalPurchaseDollars']
     vendor_sales_summary['ProfitMargin'] = vendor_sales_summary['GrossProfit'] / vendor_sales_summary['TotalSalesDollars']*100
     vendor_sales_summary['StockTurnover'] = vendor_sales_summary['TotalSalesQuantity'] / vendor_sales_summary['TotalPurchaseQuantity']
     vendor_sales_summary['SalestoPurchaseRatio'] = vendor_sales_summary['TotalSalesDollars'] / vendor_sales_summary['TotalPurchaseDollars']

return df


if_name_=='__main__'
# creating database connection
conn = sqlite3.connect('inventory.db')

logging.info ('Creating Vendor Summary Table.....')
summary_df = create_vendor_summary(conn)
logging.info(summary_df.head())

loggingg.info('Cleaning Data.....')
clean_df = clean_data(summary_df)
logging.info(clean_df.head())

logging.info('Ingesting data.....')
ingest_db(clean_df,'vendor_sales_summary',conn)
logging.info ('completed')S
    