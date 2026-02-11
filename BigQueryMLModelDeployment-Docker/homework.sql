taxinyride_2024

DROP TABLE IF EXISTS `bigquerydemo-dezoomcamp.nytaxi.external_yellow_tripdata_2024`;

CREATE OR REPLACE EXTERNAL TABLE `bigquerydemo-dezoomcamp.nytaxi.external_yellow_tripdata_2024`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://taxinyride_2024/yellow_tripdata_2024-*.parquet']
);

SELECT * FROM `bigquerydemo-dezoomcamp.nytaxi.external_yellow_tripdata_2024` LIMIT 10;

--Question1
Question 1. What is count of records for the 2024 Yellow Taxi Data? (1 point)
SELECT count(*) from `bigquerydemo-dezoomcamp.nytaxi.external_yellow_tripdata_2024`
41169720 which is double of 20,332,093

SELECT 
  _FILE_NAME as file_path, 
  COUNT(*) as rows_per_file
FROM `bigquerydemo-dezoomcamp.nytaxi.external_yellow_tripdata_2024`
GROUP BY 1;

--Question2
Question 2. What is the estimated amount of data that will be read when this query is executed on the External Table and the Table? (1 point)

--SCAN 0B
SELECT * FROM `bigquerydemo-dezoomcamp.nytaxi.external_yellow_tripdata_2024` 

CREATE OR REPLACE TABLE `bigquerydemo-dezoomcamp.nytaxi.yellow_tripdata_2024_non_partitioned`
AS
SELECT * FROM `bigquerydemo-dezoomcamp.nytaxi.external_yellow_tripdata_2024`;

--SCAN 5.5 GB
SELECT * FROM `bigquerydemo-dezoomcamp.nytaxi.yellow_tripdata_2024_non_partitioned`

Question 4. How many records have a fare_amount of 0? (1 point)
SELECT count(*) FROM `bigquerydemo-dezoomcamp.nytaxi.external_yellow_tripdata_2024` where fare_amount=0
17260 

Question 6. Write a query to retrieve the distinct VendorIDs between tpep_dropoff_datetime 2024-03-01 and 2024-03-15 (inclusive). Use the materialized table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 5 and note the estimated bytes processed. What are these values? (1 point)

--628.2 MB Scan
SELECT DISTINCT(VendorID)
FROM bigquerydemo-dezoomcamp.nytaxi.yellow_tripdata_2024_non_partitioned
WHERE DATE(tpep_pickup_datetime) BETWEEN '2024-03-01' AND '2024-03-15';

-- Create a partitioned table from external table
CREATE OR REPLACE TABLE bigquerydemo-dezoomcamp.nytaxi.yellow_tripdata_2024_partitioned
PARTITION BY
  DATE(tpep_pickup_datetime) AS
SELECT * FROM bigquerydemo-dezoomcamp.nytaxi.external_yellow_tripdata_2024;

-- Impact of partition
-- Scanning 26.85 MB of data
SELECT DISTINCT(VendorID)
FROM bigquerydemo-dezoomcamp.nytaxi.yellow_tripdata_2024_partitioned
WHERE DATE(tpep_pickup_datetime) BETWEEN '2024-03-01' AND '2024-03-15';

