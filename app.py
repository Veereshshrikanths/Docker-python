#!/usr/bin/env python3
"""
Python app that connects to PostgreSQL, creates a table,
inserts one row, and prints results in table format.
"""

import time
import sys
import psycopg2
from psycopg2 import OperationalError

# ----------- HARDCODED DB SETTINGS ------------
DB_HOST = "postgres"
DB_PORT = 5432
DB_NAME = "testdb"
DB_USER = "testuser"
DB_PASSWORD = "testpass"

TABLE_NAME = "students"


def wait_for_db(max_attempts=30, delay=1):
    """Retry until database is ready."""
    print("ready for postgresql connection....")
    for attempt in range(1, max_attempts + 1):
        try:
            conn = psycopg2.connect(
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT,
                connect_timeout=3
            )
            conn.close()
            print("connect successfully.")
            return True
        except OperationalError:
            time.sleep(delay)
    return False


def print_table_header():
    print("+----+----------+------------+------------+------------------------+")
    print("| ID | Name     | Course     | Duration   | Email ID               |")
    print("+----+----------+------------+------------+------------------------+")


def print_table_row(row):
    id, name, course, duration, email = row
    print(f"| {id:<2} | {name:<8} | {course:<10} | {duration:<10} | {email:<22} |")
    print("+----+----------+------------+------------+------------------------+")


def main():
    if not wait_for_db():
        print("ERROR: Could not connect to database.")
        sys.exit(1)

    print("connected to database")

    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

    with conn:
        with conn.cursor() as cur:

            # 1) Create table
            cur.execute(f"""
                CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    course TEXT NOT NULL,
                    duration TEXT NOT NULL,
                    email TEXT NOT NULL
                );
            """)

            # 2) Insert one row
            name = "Veeresh"
            course = "Python"
            duration = "3 Months"
            email = "veeresh@test.com"

            cur.execute(
                f"INSERT INTO {TABLE_NAME} (name, course, duration, email) VALUES (%s, %s, %s, %s) RETURNING id;",
                (name, course, duration, email)
            )
            new_id = cur.fetchone()[0]

            # 3) Read inserted row
            cur.execute(
                f"SELECT id, name, course, duration, email FROM {TABLE_NAME} WHERE id = %s;",
                (new_id,)
            )
            row = cur.fetchone()

            # 4) Print data list in table format
            print("data list:\n")
            print_table_header()
            print_table_row(row)

    conn.close()


if __name__ == "__main__":
    main()
