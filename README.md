
Dockerized Python + PostgreSQL Project  
A complete beginner‑friendly project that demonstrates how to:

 Create a simple Python application  
 Connect to PostgreSQL  
 Create a table and insert data  
 Print results in a formatted table  
 Dockerize the application  
 Run Python + PostgreSQL on a **custom Docker network**  
 Push your image to **Docker Hub**

---

#  Project Structure

```
python-docker/
├─ app.py
├─ requirements.txt
├─ Dockerfile
├─ README.md
```

---

# Python App (app.py)

This app:

 Waits for PostgreSQL  
 Connects  
 Creates table `students`  
 Inserts a row (`name, course, duration, email`)  
 Prints results in an ASCII table  

Output format:

```
ready for postgresql connection....
connect successfully.
connected to database
data list:

+----+----------+------------+------------+------------------------+
| ID | Name     | Course     | Duration   | Email ID               |
+----+----------+------------+------------+------------------------+
| 1  | veeresh    | Python     | 3 Months   | veeresh@test.com         |
+----+----------+------------+------------+------------------------+
```

---

# requirements.txt

```
psycopg2-binary==2.9.10
```

---

#  Dockerfile

A minimal Python + psycopg2 environment for running the app.

---

#  Step‑by‑Step Instructions

## 1 Build App Image

```
docker build -t my-python-app .
```

---

## 2 Create Custom Docker Network

```
docker network create my-net
```

---

## 3 Run PostgreSQL on Custom Network  
Use `--network-alias postgres` so the app can reach it using hostname `postgres`

```
docker run -d   --name my-postgres   --network my-net   --network-alias postgres   -e POSTGRES_DB=testdb   -e POSTGRES_USER=testuser   -e POSTGRES_PASSWORD=testpass   -p 5432:5432   postgres:15
```

---

## Run the Python App (one‑line)

```
docker run --rm --name my-app --network my-net my-python-app
```

---

#  Expected Output

```
ready for postgresql connection....
connect successfully.
connected to database
data list:

+----+----------+------------+------------+------------------------+
| ID | Name     | Course     | Duration   | Email ID               |
+----+----------+------------+------------+------------------------+
| 1  | veeresh   | Python     | 3 Months   | veeresh@test.com         |
+----+----------+------------+------------+------------------------+
```

---

#  Troubleshooting

### Error:  
`psycopg2.OperationalError: could not translate host name "postgres"`

### Fix:
Ensure Postgres runs with:

```
--network my-net --network-alias postgres
```

OR update `DB_HOST` in `app.py` to match container name.

---

#  Push Image to Docker Hub (Step‑by‑Step)

## Log In

```
docker login
```

## Tag Image

```
docker tag my-python-app:latest <username>/my-python-app:latest
```

Example:

```
docker tag my-python-app:latest alice/my-python-app:latest
```

## 3 Push to Docker Hub

```
docker push <username>/my-python-app:latest
```

## 4 Verify by Pulling

```
docker pull <username>/my-python-app:latest
```

---

# Cleanup

```
docker stop my-postgres
docker rm my-postgres
docker network rm my-net
```

Optional remove images:

```
docker rmi my-python-app
docker rmi <username>/my-python-app:latest
```

---


This project gives you hands‑on experience with:

 Python + PostgreSQL integration  
 Dockerfile creation  
 Custom Docker networks  
 Multi‑container communication  
 Docker Hub publishing  
