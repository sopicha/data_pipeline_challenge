How to setup:
- run at terminal in the framework directory: docker compose up airflow-init
- then run: docker compose up
- open Airflow web interface via http://localhost:8087 
- insert username: airflow, password: airflow
- At the menu bar click Admin > Connections
- You can change the post number of PostgreSQL and name by going to the menu bar > Admin > Connections
- toggle DAG: postgres_operator_1 to create a table with columns
- toggle DAG: postgres_operator_2 to load local data to PostgreSQL in Docker
