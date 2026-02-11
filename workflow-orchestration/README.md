# Kestra Workshop

This repository is based on the **Data Engineering Zoomcamp 2026 - Kestra Workshop**.  
You can find the YouTube playlist [here](https://www.youtube.com/watch?v=wgPxC4UjoLM&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=10).  
Learn more about Kestra [here](https://kestra.io/#).

---

## Pre-requisites: Python

### 1. Create the Project Folder
Create a folder `/workflow-orchestration` under the Codespace `/workspaces/kestra-workshop`.

### 2. Initialize the Project
Run the following command to initialize the project using `uv`:
```bash
uv init --python 3.13
```

### 3. Create the Virtual Environment
Check the Python version to confirm the virtual environment is created:
```bash
uv run python -V
```

### 4. Activate the Virtual Environment
Activate the virtual environment:
```bash
source .venv/bin/activate
```

### 5. Add Required Packages
Install the required packages using `uv`:
```bash
uv add pandas
uv add pyarrow
uv add pgcli
uv add sqlalchemy psycopg2-binary
uv add tqdm
uv add python-dotenv
```

### 6. View Installed Packages
List the installed packages:
```bash
uv pip list
```
Example output:
| Package           | Version   |
|-------------------|-----------|
| pandas            | 3.0.0     |
| pgcli             | 4.4.0     |
| psycopg2-binary   | 2.9.11    |
| pyarrow           | 23.0.0    |
| sqlalchemy        | 2.0.46    |
| tqdm              | 4.67.3    |

---

## Pre-requisites: Docker

### 1. Create the Docker Network
Create a Docker network:
```bash
docker network create pg-network_kestra
```

Verify the network exists:
```bash
docker network ls
```
Example output:
| NETWORK ID     | NAME                | DRIVER    | SCOPE |
|----------------|---------------------|-----------|-------|
| 250dad1aff81   | pg-network_kestra   | bridge    | local |

### 2. Set Up `docker-compose.yaml`
Update the `docker-compose.yaml` file to include the required services.

---

## Execute: Docker

### 1. Start the Containers
Run the following command from the `/workflow-orchestration` directory:
```bash
docker-compose up
```

### 2. Set Up the Database Server
Access **pgAdmin4** in your browser at:  
[http://127.0.0.1:8085/browser/](http://127.0.0.1:8085/browser/)

- **Server Name**: kestra  
- **Connection Name**: pg-database-kestra  
- **Port**: 5432  
- **Maintenance Database**: postgres  
- **Username**: root  

Once the database server is set up, browse to:  
`Servers -> Kestra -> Databases -> ny_taxi -> Schemas -> public -> Tables`

### 3. Access the PostgreSQL Database
In a separate terminal, run the following command to access the `postgres:18` container:
```bash
uv run pgcli -h localhost -p 5432 -u root -d ny_taxi
```

Check the tables:
```sql
\dt
```
Example output:
| Schema | Name | Type | Owner |
|--------|------|------|-------|
| (none) | (none) | (none) | (none) |

---

## Setup: Data Ingestion Pipeline

### 1. Create the Ingestion Script
Set up the `ingest_data.py` script to handle data ingestion.

### 2. Run the Ingestion Script
Run the script to insert data into the PostgreSQL container:
```bash
uv run python ingest_data.py \
   --pg-user=root \
   --pg-password=root \
   --pg-host=localhost \
   --pg-port=5432 \
   --pg-db=ny_taxi \
   --target-table=yellow_taxi_data \
   --year=2021 \
   --month=1 \
   --chunksize=100000
```

### 3. Verify the Data Load
Check the tables:
```sql
\dt
```
Example output:
| Schema | Name             | Type  | Owner |
|--------|------------------|-------|-------|
| public | yellow_taxi_data | table | root  |

Count the rows in the table:
```sql
SELECT count(*) FROM yellow_taxi_data;
```
Example output:
| count   |
|---------|
| 1369765 |

---

## Kestra Setup

### 1. Update `docker-compose.yaml`
Add the following entries to the `docker-compose.yaml` file:
- `kestra_postgres`
- `kestra`

Also, add two additional volumes.

### 2. Start the Containers
Start the containers:
```bash
docker-compose up
```

Verify the running containers:
```bash
docker ps -a
```
Example output:
| CONTAINER ID   | IMAGE                | STATUS          | PORTS                     | NAMES                                   |
|----------------|----------------------|-----------------|---------------------------|-----------------------------------------|
| e77595234376   | kestra/kestra:v1.1   | Up 5 minutes    | 8080-8081/tcp             | workflow-orchestration-kestra-1         |
| 41f05dacb410   | postgres:18          | Up 5 minutes    | 5432/tcp                  | workflow-orchestration-kestra_postgres-1|
| 4755ab9c0911   | dpage/pgadmin4       | Up 5 minutes    | 8085/tcp                  | workflow-orchestration-pgadmin-1        |
| 2a4579040b82   | postgres:18          | Up 5 minutes    | 5432/tcp                  | workflow-orchestration-pg-database-kestra-1 |

### 3. Access the UI
- **pgAdmin4**: [http://127.0.0.1:8085/browser/](http://127.0.0.1:8085/browser/)  
- **Kestra UI**: [http://127.0.0.1:8080/ui/login?from=/dashboards](http://127.0.0.1:8080/ui/login?from=/dashboards)

### 4. Set Up Flows
Place `.yaml` files under the `/flows` folder in the Kestra server and execute them.

---

## Summary of Containers

| Container ID   | Image                | Description                                      |
|----------------|----------------------|--------------------------------------------------|
| `4755ab9c0911` | `dpage/pgadmin4`     | pgAdmin container (Access pgAdmin UI)           |
| `2a4579040b82` | `postgres:18`        | PostgreSQL database container                   |
| `41f05dacb410` | `postgres:18`        | Kestra metadata database container              |
| `e77595234376` | `kestra/kestra:v1.1` | Kestra server container (Access Kestra UI)      |
