#!/usr/bin/env python
# coding: utf-8
"""This script ingests NYC taxi data into a Postgres database in chunks to handle large datasets efficiently."""

import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm
import click

def ingest_data(url: str, engine, target_table: str, chunksize: int = 100000):
    """Ingest data into Postgres database"""

    dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
    }
    
    parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
      ]
    
    df = pd.read_csv(url,dtype=dtype,parse_dates=parse_dates)

    """Get the DDL Schema for the database """
    print(pd.io.sql.get_schema(df, name=target_table, con=engine))

    """Create an empty table with the name yellow_taxi_data but without any data , empty dataframe/table"""
    df.head(0).to_sql(name=target_table,con=engine,if_exists="replace")

    """Instead of inserting all the data at once, where the data is stored in the memory and then retrieved, iterate the data chunk by chunk and insert it"""
    """df_iter is an iterator object"""
    df_iter=pd.read_csv(url,dtype=dtype,parse_dates=parse_dates,iterator=True,chunksize=chunksize)

    for df_chunk in tqdm(df_iter):
       df_chunk.to_sql(name=target_table,con=engine,if_exists="append")
       """It will take 12 chunks of data for insert"""

@click.command()
@click.option('--year', type=int, default=2021, help='Year for the taxi data')
@click.option('--month', type=int, default=1, help='Month for the taxi data')
@click.option('--pg-user', default='root', help='PostgreSQL username')
@click.option('--pg-password', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default='5432', help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--target-table', default='yellow_taxi_data', help='Target table name')
@click.option('--chunksize', type=int, default=100000, help='Chunk size for data ingestion')
def main(year, month, pg_user, pg_password, pg_host, pg_port, pg_db, target_table, chunksize):
    """Ingest NYC taxi data into PostgreSQL"""

    engine = create_engine(f'postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}')
    prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
    url=f"{prefix}/yellow_tripdata_{year:04d}-{month:02d}.csv.gz"

    ingest_data(
        url=url,
        engine=engine,
        target_table=target_table,
        chunksize=chunksize
    )

if __name__=="__main__":
    main()