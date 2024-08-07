import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('APAN5310_HW6_DATA.csv')

#data exploration
df.info()

#data cleaning
print("The total NA value in Date Recorded: ", df['Date Recorded'].isna().sum())  # check NA values
print("The total NA value in Address: ", df['Address'].isna().sum())
print("The total NA value in Residential Type: ", df['Residential Type'].isna().sum())

df = df.dropna(subset=['Residential Type'])
df = df.dropna(subset=['Address'])
df.info()

#remove irrelevant columns
variables_remove = ["List Year", "Property Type", "Non Use Code", "Assessor Remarks", "OPM remarks", "Location"]
df = df.drop(columns=variables_remove)
df.info()

#remove anomaly
df_cleaned = df[
    (df['Town'] != "***Unknown***") &
    (df['Sale Amount'] > 30000)
].copy()

#transform date format
df_cleaned.loc[:, 'Date Recorded'] = pd.to_datetime(df_cleaned['Date Recorded'], format='%m/%d/%Y').dt.strftime('%Y-%m-%d')

#data validation
df_cleaned.head()
df_cleaned.info()

import numpy as np
import random

#data transformation
# Randomly assign status
statuses = np.random.choice(
    ['SOLD', 'LEASED', 'PENDING'], 
    size=len(df_cleaned), 
    p=[0.7, 0.2, 0.1]
)

df_cleaned['Status'] = statuses

# Set sale_amount and sales_ratio to NULL for LEASED and PENDING
df_cleaned.loc[df_cleaned['Status'].isin(['LEASED', 'PENDING']), ['Sale Amount', 'Sales Ratio']] = None

df_cleaned['State'] = 'CT'

#remove anomaly
df_cleaned = df_cleaned[df_cleaned['Sale Amount'].isnull() | (df_cleaned['Sale Amount'] < 10**8)]
df_cleaned = df_cleaned[df_cleaned['Assessed Value'].isnull() | (df_cleaned['Assessed Value'] < 10**8)]
# Limit the DataFrame to 1000 rows
df_cleaned = df_cleaned.head(1000)

#data validation
df_cleaned.info()

from sqlalchemy import create_engine

# Database connection parameters
db_url = "postgresql+psycopg2://postgres:123@localhost:5432/Dream_Homes_NYC"
engine = create_engine(db_url)
conn = engine.connect()


# Rename columns in the DataFrame for insertion
df_cleaned = df_cleaned.rename(columns={
    'Serial Number': 'home_id',
    'Address': 'address',
    'Town': 'city',
    'State': 'state',
    'Date Recorded': 'date_recorded',
    'Assessed Value': 'assessed_value',
    'Sale Amount': 'sale_amount',
    'Sales Ratio': 'sales_ratio',
    'Residential Type': 'type',
    'Status': 'status'
})


# Insert data into Homes
insert_query = """
INSERT INTO Homes (home_id, address, city, state, date_recorded, assessed_value, sale_amount, sales_ratio, type, status)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (home_id) DO NOTHING;
"""

try:
    for index, row in df_cleaned.iterrows():
        conn.execute(insert_query, (
            row['home_id'], 
            row['address'], 
            row['city'], 
            row['state'], 
            row['date_recorded'], 
            row['assessed_value'], 
            row['sale_amount'], 
            row['sales_ratio'], 
            row['type'], 
            row['status']
        ))
    conn.execute("COMMIT")
    print("Data loaded successfully into the Homes table.")
except Exception as e:
    conn.execute("ROLLBACK")
    print(f"An error occurred: {e}")

