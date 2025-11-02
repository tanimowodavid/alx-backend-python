import mysql.connector
import csv
import uuid
from mysql.connector import Error

# Connect to MySQL server (no database yet)
def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="yourpassword"  # replace with your actual password
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None


# Create the ALX_prodev database if it doesn't exist
def create_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        connection.commit()
        cursor.close()
        print("Database ALX_prodev created successfully (if it didn't exist).")
    except Error as e:
        print(f"Error creating database: {e}")


# Connect directly to the ALX_prodev database
def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="yourpassword",  # replace with your actual password
            database="ALX_prodev"
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to ALX_prodev: {e}")
        return None


# Create the user_data table if it doesn’t exist
def create_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id CHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL(3,0) NOT NULL,
                INDEX (user_id)
            );
        """)
        connection.commit()
        cursor.close()
        print("Table user_data created successfully.")
    except Error as e:
        print(f"Error creating table: {e}")


# Insert data from CSV if not already inserted
def insert_data(connection, csv_file):
    try:
        cursor = connection.cursor()
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                cursor.execute("""
                    INSERT INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                """, (str(uuid.uuid4()), row['name'], row['email'], row['age']))
        connection.commit()
        cursor.close()
        print("Data inserted successfully from CSV.")
    except Error as e:
        print(f"Error inserting data: {e}")
    except FileNotFoundError:
        print("CSV file not found.")
