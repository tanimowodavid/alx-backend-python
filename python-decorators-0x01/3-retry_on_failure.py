import time
import sqlite3 
import functools

#### paste your with_db_decorator here
def with_db_connection(func):
    """ your code goes here""" 
    @functools.wraps(func) 
    def wrapper(*args, **kwargs): 
        conn = sqlite3.connect('users.db')
        try: 
            result = func(conn, *args, **kwargs) 
        finally:
            if conn:
                conn.close() 
        return result 
    return wrapper

#### decorator to retry on failure
""" your code goes here"""
def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except (sqlite3.OperationalError, ConnectionError) as e:
                    # Catch only transient errors, not all exceptions
                    last_exception = e
                    print(f"Attempt {attempt} failed: {e}. Retrying in {delay} seconds...")
                    time.sleep(delay)
            print("All retry attempts failed.")
            raise last_exception
        return wrapper
    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)

def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)