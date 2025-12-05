Dockerized Python + PostgreSQL Example

A simple end-to-end project that:

Runs PostgreSQL in a container on a custom Docker network.

Runs a Python app in a container on the same network.

The app:

waits for the DB,

creates a table students,

inserts one row with name, course, duration, email,

prints status messages and the data in an ASCII table format.

This README gives detailed, step-by-step instructions to build, run and troubleshoot the project.

Project files
docker-pg-simple/
├─ app.py
├─ requirements.txt
├─ Dockerfile
├─ README.md   <-- you are reading this


app.py is the app that connects to PostgreSQL (hard-coded settings), creates the table, inserts one row and prints the output in the format you requested:

ready for postgresql connection....
connect successfully.
connected to database
data list:

+----+----------+------------+------------+------------------------+
| ID | Name     | Course     | Duration   | Email ID               |
+----+----------+------------+------------+------------------------+
| 1  | Alice    | Python     | 3 Months   | alice@test.com         |
+----+----------+------------+------------+------------------------+

Prerequisites

Docker installed and running on your machine.

(Optional) docker-compose if you prefer compose (instructions included below).

Basic shell/terminal familiarity.

1 — Build the app image

From the project root (where Dockerfile is located) run:

docker build -t my-python-app .


This produces an image named my-python-app that contains Python and the app code.

2 — Create a custom Docker network

Create a user-defined bridge network (so containers resolve each other by name / alias):

docker network create my-net


Check it exists:

docker network ls

3 — Run PostgreSQL container (recommended command)

Run Postgres attached to the custom network and give it a DNS alias postgres (so the app — which uses DB_HOST = "postgres" by default — can resolve it):

docker run -d \
  --name my-postgres \
  --network my-net \
  --network-alias postgres \
  -e POSTGRES_DB=testdb \
  -e POSTGRES_USER=testuser \
  -e POSTGRES_PASSWORD=testpass \
  -p 5432:5432 \
  postgres:15


What this does:

--name my-postgres sets the container name.

--network my-net connects it to the custom network.

--network-alias postgres creates the DNS name postgres on my-net so the app can use postgres as the host.

-e ... sets database name / user / password for Postgres initialization.

-p 5432:5432 exposes Postgres on the host (optional; remove if you don't need host access).

If you prefer to run the container with the literal name postgres (so the alias is unnecessary), use --name postgres instead of --name my-postgres --network-alias postgres.

4 — Run the app container (one-line)

Use the one-line command you asked for:

docker run --rm --name my-app --network my-net my-python-app


--rm removes the app container after it exits.

The app will print status messages and the ASCII table containing the inserted row.

5 — Expected output (example)

When everything is working you should see a sequence similar to:

ready for postgresql connection....
connect successfully.
connected to database
data list:

+----+----------+------------+------------+------------------------+
| ID | Name     | Course     | Duration   | Email ID               |
+----+----------+------------+------------+------------------------+
| 1  | Alice    | Python     | 3 Months   | alice@test.com         |
+----+----------+------------+------------+------------------------+


If the DB is still initializing, the app prints the waiting messages and will retry until the DB responds.

Troubleshooting
Error: psycopg2.OperationalError: could not translate host name "postgres" to address

Meaning: the app container could not resolve the hostname postgres.

Common causes and fixes:

Postgres container not on same network

Ensure you connected Postgres to my-net using --network my-net.

Re-run postgresql with --network my-net or connect it to the network:

docker network connect my-net my-postgres


Postgres container name/alias mismatch

The app expects DB_HOST = "postgres". You can:

Start Postgres with alias postgres (recommended):

--network-alias postgres


OR start the container with name postgres:

--name postgres


OR change app.py to use whatever name you used (e.g., my-postgres):

DB_HOST = "my-postgres"


Postgres container not running

Check with docker ps. If it's not running, inspect logs:

docker logs my-postgres


Port conflicts on host or firewall issues

If you exposed port 5432:5432 on the host and another Postgres is using it, either stop the local Postgres or omit the host port mapping.

If you see connection refused while DB initializes

This is normal. The app retries in a loop until the DB is ready.

If after many attempts it still fails, check docker logs my-postgres for Postgres start errors.

6 — Inspecting containers & logs

Show running containers:

docker ps


View Postgres logs:

docker logs -f my-postgres


View app logs (if not using --rm):

docker logs -f my-app