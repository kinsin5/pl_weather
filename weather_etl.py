import pandas as pd
import requests
import datetime

ENDPOINT = 'https://danepubliczne.imgw.pl/api/data/synop/'
response = requests.get(ENDPOINT).json()

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

from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv(override=True)

# Fetch variables
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

# Construct the SQLAlchemy connection string
DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"

# Create the SQLAlchemy engine
# engine = create_engine(DATABASE_URL)
# If using Transaction Pooler or Session Pooler, we want to ensure we disable SQLAlchemy client side pooling -
# https://docs.sqlalchemy.org/en/20/core/pooling.html#switching-pool-implementations
engine = create_engine(DATABASE_URL, poolclass=NullPool)

# Test the connection
try:
    with engine.connect() as connection:
        print("Connection successful!")
except Exception as e:
    print(f"Failed to connect: {e}")

def write_to_supabase(df):
    df.to_sql(
        name='weather',
        con=engine,
        if_exists='append',  # don't replace the table
        index=False,         # don't write the DataFrame index as a column
        method='multi'       # use bulk insert for better performance
    )
    print("✅ Data inserted into Supabase!")

write_to_supabase(df)   