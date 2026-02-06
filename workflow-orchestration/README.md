Pre-requisites Python 

1.Create a folder /workflow-orchestration under the codespace /workspaces/kestra-workshop

2.Initiliaze the project using uv 
uv init --python 3.13

3.Create the virtual environment
uv run python -V

4.Activate the virtual environment
@deepaknrn ➜ /workspaces/kestra-workshop/workflow-orchestration (main) $ pwd
/workspaces/kestra-workshop/workflow-orchestration
@deepaknrn ➜ /workspaces/kestra-workshop/workflow-orchestration (main) $ source .venv/bin/activate
(workflow-orchestration) @deepaknrn ➜ /workspaces/kestra-workshop/workflow-orchestration (main)

5.Add the packages required
uv add pandas
uv add pyarrow
uv add pgcli
uv add sqlalchemy psycopg2-binary
uv add tqdm 

6.View the list of packages 
uv pip list
Package           Version
----------------- -----------
pandas            3.0.0
pgcli             4.4.0
psycopg2-binary   2.9.11
pyarrow           23.0.0
sqlalchemy        2.0.46
tqdm              4.67.3


Pre requisites - Docker
1.Create the docker network
(workflow-orchestration) @deepaknrn ➜ /workspaces/kestra-workshop/workflow-orchestration (main) $ docker network create pg-network_kestra
250dad1aff817665d2ef4e354a72de5491fab6783cce236e80ebaf189973b192

Check if the network exists using the command 
(workflow-orchestration) @deepaknrn ➜ /workspaces/kestra-workshop/workflow-orchestration (main) $ docker network ls
NETWORK ID     NAME                DRIVER    SCOPE
2726fe9d06ce   bridge              bridge    local
db1eb6025d87   host                host      local
0a68eb645402   none                null      local
250dad1aff81   pg-network_kestra   bridge    local

2.Setup docker-compose.yaml

Execute - Docker
1.Run docker-compose up from the directory /workflow-orchestration
Setup a database server using pgadmin4
Server Name : kestra
Connection Name : pg-database-kestra
Port : 5432 
Maintainence database : postgres
Username : root
Once the database server has been setup . 
Browse via pgadmin4 in the browser to the path: 
Servers -> Kestra -> Databases -> ny_taxi -> Schemas -> public -> Tables 

2.In a separate terminal window,Run the postgres:18 container locally using :
uv run pgcli -h localhost -p 5432  -u root -d ny_taxi
There will be currently no tables or data being loaded in this database within container
Home: http://pgcli.com
root@localhost:ny_taxi> \dt
+--------+------+------+-------+
| Schema | Name | Type | Owner |
|--------+------+------+-------|
+--------+------+------+-------+
SELECT 0
Time: 0.009s

Setup Data Ingestion Pipeline
1.Setup the data ingestion script ingest_data.py

Execute the Data Ingestion Pipeline
1.Running the ingestion script from local machine(GitHub codespaces)to insert data in the postgres container target table
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

2.Verify the data load;
root@localhost:ny_taxi> \dt
+--------+------------------+-------+-------+
| Schema | Name             | Type  | Owner |
|--------+------------------+-------+-------|
| public | yellow_taxi_data | table | root  |
+--------+------------------+-------+-------+
SELECT 1
Time: 0.004s

root@localhost:ny_taxi> SELECT count(*) From yellow_taxi_data;
+---------+
| count   |
|---------|
| 1369765 |
+---------+
SELECT 1
Time: 0.133s

--KESTRA WORKSHOP--
This repo is based on Data Engineering Zoomcamp 2026 - Kestra Workshop. The youtube playlist is provided in the following link : https://www.youtube.com/watch?v=wgPxC4UjoLM&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=10

Kestra -> https://kestra.io/#

1.Update the docker-compose.yaml with 2 entries related to Kestra
kestra_postgres & kestra , Update 2 more volumes as well in the composer file

List the running containers
(workflow-orchestration) @deepaknrn ➜ /workspaces/kestra-workshop/workflow-orchestration (main) $ docker ps -a
CONTAINER ID   IMAGE            COMMAND                  CREATED          STATUS          PORTS                                              NAMES
4755ab9c0911   dpage/pgadmin4   "/entrypoint.sh"         31 minutes ago   Up 31 minutes   443/tcp, 0.0.0.0:8085->80/tcp, [::]:8085->80/tcp   workflow-orchestration-pgadmin-1
2a4579040b82   postgres:18      "docker-entrypoint.s…"   31 minutes ago   Up 31 minutes   0.0.0.0:5432->5432/tcp, [::]:5432->5432/tcp        workflow-orchestration-pg-database-kestra-1

Stop the running containers
(workflow-orchestration) @deepaknrn ➜ /workspaces/kestra-workshop/workflow-orchestration (main) $ docker stop 4755ab9c0911
4755ab9c0911
(workflow-orchestration) @deepaknrn ➜ /workspaces/kestra-workshop/workflow-orchestration (main) $ docker stop 2a4579040b82
2a4579040b82

Check the status of the containers after stopping
(workflow-orchestration) @deepaknrn ➜ /workspaces/kestra-workshop/workflow-orchestration (main) $ docker ps -a
CONTAINER ID   IMAGE            COMMAND                  CREATED          STATUS                      PORTS     NAMES
4755ab9c0911   dpage/pgadmin4   "/entrypoint.sh"         33 minutes ago   Exited (0) 38 seconds ago             workflow-orchestration-pgadmin-1
2a4579040b82   postgres:18      "docker-entrypoint.s…"   33 minutes ago   Exited (0) 30 seconds ago             workflow-orchestration-pg-database-kestra-1

Update the docker-compose.yaml with 2 additional entries related to Kestra

Start the containers again using docker-compose up

@deepaknrn ➜ /workspaces/kestra-workshop (main) $ docker ps -a
CONTAINER ID   IMAGE                COMMAND                  CREATED          STATUS                   PORTS                                                             NAMES
e77595234376   kestra/kestra:v1.1   "docker-entrypoint.s…"   5 minutes ago    Up 5 minutes             0.0.0.0:8080-8081->8080-8081/tcp, [::]:8080-8081->8080-8081/tcp   workflow-orchestration-kestra-1
41f05dacb410   postgres:18          "docker-entrypoint.s…"   5 minutes ago    Up 5 minutes (healthy)   5432/tcp                                                          workflow-orchestration-kestra_postgres-1
4755ab9c0911   dpage/pgadmin4       "/entrypoint.sh"         44 minutes ago   Up 5 minutes             443/tcp, 0.0.0.0:8085->80/tcp, [::]:8085->80/tcp                  workflow-orchestration-pgadmin-1
2a4579040b82   postgres:18          "docker-entrypoint.s…"   44 minutes ago   Up 5 minutes             0.0.0.0:5432->5432/tcp, [::]:5432->5432/tcp                       workflow-orchestration-pg-database-kestra-1

Now we have 4 containers up and running 

4755ab9c0911 -> pgadmin container (Accessing pgadmin)
2a4579040b82 -> postgres database (Accessing postgresdatabase via terminal bash using uv run)
41f05dacb410 -> kestra_postgres container [to store the data/metadata related to kestra]
e77595234376 -> kestra/kestra:v1.1 container (Acessing kestra related infromation Kestra UI , Kestra Server)

*** UI Links ***
http://127.0.0.1:8085/browser/ -> pgadmin4
http://127.0.0.1:8080/ui/login?from=/dashboards -> Kestra UI , Kestra Server

Setup the .yaml files under folder /flows in the Kestra Server and try executing it.
