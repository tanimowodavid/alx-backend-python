import mysql.connector
from mysql.connector import Error

def stream_users():
    """Generator that yields rows from the user_data table one by one"""
    try:
        # Connect to the ALX_prodev database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="yourpassword",   # replace with your real password
            database="ALX_prodev"
        )

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM user_data;")

            # yield each row one by one
            for row in cursor:
                yield row

            cursor.close()
            connection.close()

    except Error as e:
        print(f"Error: {e}")
        return
