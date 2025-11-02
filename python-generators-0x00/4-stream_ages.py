import seed


def stream_user_ages():
    """
    Generator that yields user ages one by one from the database.
    Uses a single loop to stream results.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")
    for (age,) in cursor:
        yield age
    cursor.close()
    connection.close()


def calculate_average_age():
    """
    Uses the generator to compute the average age 
    without loading all rows into memory.
    """
    total = 0
    count = 0
    for age in stream_user_ages():
        total += age
        count += 1

    average_age = total / count if count > 0 else 0
    print(f"Average age of users: {average_age:.2f}")


if __name__ == "__main__":
    calculate_average_age()
