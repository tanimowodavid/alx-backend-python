import mysql.connector
from mysql.connector import Error

def stream_users_in_batches(batch_size):
    """Generator that yields users in batches from the user_data table"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="yourpassword",  # replace with your password
            database="ALX_prodev"
        )

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM user_data;")

            batch = []
            for row in cursor:
                batch.append(row)
                if len(batch) == batch_size:
                    yield batch
                    batch = []  # reset batch after yielding

            # yield any remaining rows
            if batch:
                yield batch

            cursor.close()
            connection.close()

    except Error as e:
        print(f"Error: {e}")
        return


def batch_processing(batch_size):
    """Process each batch to filter users over age 25"""
    for batch in stream_users_in_batches(batch_size):
        processed = [user for user in batch if int(user["age"]) > 25]
        for user in processed:
            print(user)
