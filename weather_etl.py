import pandas as pd
import requests
import datetime
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
import os

# Fetch data from the endpoint
ENDPOINT = 'https://danepubliczne.imgw.pl/api/data/synop/'
response = requests.get(ENDPOINT).json()

# Prepare DataFrame
df = pd.DataFrame(response)
df['data_pomiaru'] = df['data_pomiaru'] + ' ' + df['godzina_pomiaru']
df['data_pomiaru'] = pd.to_datetime(df['data_pomiaru'])
df = df.drop(columns=['godzina_pomiaru'])

# Define the conversion dictionary
convert_dict = {'id_stacji':int, 'temperatura':float, 'predkosc_wiatru':int, 'kierunek_wiatru':int, 
                'wilgotnosc_wzgledna':float, 'suma_opadu':float, 'cisnienie':float
            }
# Convert columns using the dictionary
df = df.astype(convert_dict)

# Fetch environment variables from GitHub Secrets
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST")
PORT = os.getenv("DB_PORT")
DBNAME = os.getenv("DB_NAME")

# Construct the SQLAlchemy connection string
DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, poolclass=NullPool)

# Test the connection
try:
    with engine.connect() as connection:
        print("Connection successful!")
except Exception as e:
    print(f"Failed to connect: {e}")

# Function to write DataFrame to Supabase
def write_to_supabase(df):
    df.to_sql(
        name='weather',
        con=engine,
        if_exists='append',  # don't replace the table
        index=False,         # don't write the DataFrame index as a column
        method='multi'       # use bulk insert for better performance
    )
    print("✅ Data inserted into Supabase!")

# Insert data
write_to_supabase(df)
